from rest_framework import serializers
from .models import Month, MonthHero, Mentor, Direction, News


class MonthHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthHero
        fields = [
            'id', 'month', 'hero_type', 'title', 'description',
            'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MonthSerializer(serializers.ModelSerializer):
    heroes = MonthHeroSerializer(many=True, read_only=True)

    class Meta:
        model = Month
        fields = ['id', 'name', 'is_active', 'heroes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = [
            'id', 'full_name', 'title', 'description',
            'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = [
            'id', 'title', 'description',
            'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'title', 'description',
            'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
