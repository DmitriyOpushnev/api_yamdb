from rest_framework import serializers

from reviews.models import Category, Genre, User


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


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
