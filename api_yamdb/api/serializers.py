from rest_framework import serializers

from reviews.models import Category, Genre


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


class TitleGetSerializer(serializers.ModelSerializer):  # похоже так
    rating = serializers.IntegerField()

    class Meta:
        read_only_fields = ('rating',)
