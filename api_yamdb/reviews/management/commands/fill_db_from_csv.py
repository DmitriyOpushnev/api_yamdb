import csv
from django.core.management.base import BaseCommand
from pathlib import Path
from reviews.models import Category, Genre, Title, User, Review, Comment


class Command(BaseCommand):
    help = 'Fills the database with data from csv-file in static folder'
    CSV_DIR = Path('static', 'data')

    def handle(self, *args, **kwargs):
        FILE_FOO = (
            ('category.csv', self.import_cats_genres_users),
            ('genre.csv', self.import_cats_genres_users),
            ('users.csv', self.import_cats_genres_users),
            ('titles.csv', self.import_titles),
            ('genre_title.csv', self.add_genre_to_titles),
            ('review.csv', self.import_reviews),
            ('comments.csv', self.import_comments),
        )

        for file, foo in FILE_FOO:
            self.stdout.write(f'Начинаем импорт из файла {file}')
            with open(Path(self.CSV_DIR, file), encoding='utf8') as f:
                reader = csv.DictReader(f)
                foo(reader, file)

    def import_cats_genres_users(self, reader, file):
        DATA = {
            'category.csv': (Category, ['id', 'name', 'slug']),
            'genre.csv': (Genre, ['id', 'name', 'slug']),
            'users.csv': (User, ['id', 'username', 'email', 'role', 'bio',
                                 'first_name', 'last_name']),
        }
        counter = 0
        objects_to_create = []
        for row in reader:
            counter += 1
            atrs = {field: row[field] for field in DATA[file][1]}
            objects_to_create.append(DATA[file][0](**atrs))
        DATA[file][0].objects.bulk_create(objects_to_create,
                                          ignore_conflicts=True)
        self.stdout.write(f'Добавлено объектов: {len(objects_to_create)}; '
                          f'строк в документе: {counter}')

    def import_titles(self, reader, file):
        counter = 0
        objects_to_create = []
        for row in reader:
            counter += 1
            try:
                category = Category.objects.get(id=row['category'])
            except Exception:
                category = None
                self.stderr.write(f'Категория {row["category"]} не найдена')
            objects_to_create.append(Title(id=row['id'],
                                           name=row['name'],
                                           year=row['year'],
                                           category=category))
        Title.objects.bulk_create(objects_to_create, ignore_conflicts=True)
        self.stdout.write(f'Добавлено объектов: {len(objects_to_create)}; '
                          f'строк в документе: {counter}')

    def add_genre_to_titles(self, reader, file):
        counter = 0
        objects_to_create = []
        for row in reader:
            counter += 1
            try:
                genre = Genre.objects.get(id=row['genre_id'])
            except Genre.DoesNotExist:
                self.stderr.write(f'Genre №{row["genre_id"]} не найден')
                continue
            try:
                title = Title.objects.get(id=row['title_id'])
            except Exception:
                self.stderr.write(f'Title №{row["title_id"]} не найден')
                continue
            objects_to_create.append(
                Title.genre.through(id=row['id'], title=title, genre=genre)
            )
        Title.genre.through.objects.bulk_create(objects_to_create,
                                                ignore_conflicts=True)
        self.stdout.write(f'Добавлено связей: {len(objects_to_create)}; '
                          f'строк в документе: {counter}')

    def import_reviews(self, reader, file):
        counter = 0
        objects_to_create = []
        for row in reader:
            counter += 1
            try:
                title = Title.objects.get(id=row['title_id'])
            except Exception:
                self.stderr.write(f'Title №{row["title_id"]} не найден')
                continue
            try:
                author = User.objects.get(id=row['author'])
            except Exception:
                self.stderr.write(f'User №{row["author"]} не найден')
                continue
            objects_to_create.append(Review(id=row['id'],
                                            title=title,
                                            text=row['text'],
                                            author=author,
                                            score=row['score'],
                                            pub_date=row['pub_date']))
        Review.objects.bulk_create(objects_to_create, ignore_conflicts=True)
        self.stdout.write(f'Добавлено объектов: {len(objects_to_create)}; '
                          f'строк в документе: {counter}')

    def import_comments(self, reader, file):
        counter = 0
        objects_to_create = []
        for row in reader:
            counter += 1
            try:
                review = Review.objects.get(id=row['review_id'])
            except Exception:
                self.stderr.write(f'Review №{row["review_id"]} не найден')
                continue
            try:
                author = User.objects.get(id=row['author'])
            except Exception:
                self.stderr.write(f'User №{row["author"]} не найден')
                continue
            objects_to_create.append(Comment(id=row['id'],
                                             review=review,
                                             text=row['text'],
                                             author=author,
                                             pub_date=row['pub_date']))
        Comment.objects.bulk_create(objects_to_create, ignore_conflicts=True)
        self.stdout.write(f'Добавлено объектов: {len(objects_to_create)}; '
                          f'строк в документе: {counter}')
