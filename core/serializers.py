from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Month, MonthHero, Mentor, Direction, News


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class MonthHeroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    month_name = serializers.CharField(source='month.name', read_only=True)

    class Meta:
        model = MonthHero
        fields = [
            'id', 'month', 'month_name', 'user', 'type',
            'image', 'description', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MonthSerializer(serializers.ModelSerializer):
    heroes = MonthHeroSerializer(many=True, read_only=True)

    class Meta:
        model = Month
        fields = ['id', 'name', 'description', 'is_active', 'heroes', 'created_at']
        read_only_fields = ['id', 'created_at']


class MentorSerializer(serializers.ModelSerializer):
    direction_title = serializers.CharField(source='direction.title', read_only=True, allow_null=True)

    class Meta:
        model = Mentor
        fields = [
            'id', 'full_name', 'direction', 'direction_title',
            'image', 'description', 'bio', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DirectionSerializer(serializers.ModelSerializer):
    mentors = MentorSerializer(many=True, read_only=True)

    class Meta:
        model = Direction
        fields = [
            'id', 'title', 'description',
            'is_active', 'mentors', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'title', 'content',
            'image', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']