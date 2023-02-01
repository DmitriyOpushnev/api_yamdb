from rest_framework import serializers
from django.utils import timezone

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class AbstractTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        return 9          #  ждем модель Review


class GetTitleSerializer(AbstractTitleSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)


class PostTitleSerializer(AbstractTitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def validate(self, data):
        # тут было только условие на >, но в pytest падает 1 тест при патч-запросе, где None (нет года в data) нельзя сравнить с int (год)
        # при добавлении условия на наличие year ошибка ушла, но падают другие тесты с рейтингом; при тестах через postman все работает нормально без доп.условия 
        # доведу до рабочего состояния, когда будут рейтинги
        if data.get('year') and data.get('year') > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше текущего.'
            )
        return data
