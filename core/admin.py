from django.contrib import admin
from .models import Month, MonthHero, Mentor, Direction, News


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(MonthHero)
class MonthHeroAdmin(admin.ModelAdmin):
    list_display = ('month', 'user', 'type', 'is_active', 'created_at')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username', 'month__name')
    ordering = ('-created_at',)


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('full_name',)
    ordering = ('-created_at',)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('-created_at',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('-created_at',)
