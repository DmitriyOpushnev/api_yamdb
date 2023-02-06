from django.contrib import admin

from reviews.models import Category, Genre, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    exclude = [
        'last_login', 'is_staff',
        'is_active', 'date_joined',
        'groups', 'user_permissions',
        'password'
    ]
    search_fields = ('username',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
