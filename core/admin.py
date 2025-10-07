from django.contrib import admin
from django.utils.html import format_html
from .models import Month, MonthHero, Mentor, Direction, News


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(MonthHero)
class MonthHeroAdmin(admin.ModelAdmin):
    list_display = ('month', 'user', 'type', 'image_preview', 'is_active', 'created_at')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username', 'month__name')
    ordering = ('-created_at',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'direction', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'direction')
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