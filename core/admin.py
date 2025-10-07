from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.decorators import display
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
    MultipleChoicesDropdownFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from import_export.admin import ImportExportModelAdmin
from django import forms

from .models import Month, MonthHero, Mentor, Direction, News


# ============================================================================
# CUSTOM FORMS WITH ENHANCED WIDGETS
# ============================================================================

class MonthAdminForm(forms.ModelForm):
    """Custom form for Month with WYSIWYG editor"""

    class Meta:
        model = Month
        fields = '__all__'
        widgets = {
            'description': WysiwygWidget(),
        }


class NewsAdminForm(forms.ModelForm):
    """Custom form for News with WYSIWYG editor"""

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content': WysiwygWidget(),
        }


class MentorAdminForm(forms.ModelForm):
    """Custom form for Mentor with WYSIWYG editor"""

    class Meta:
        model = Mentor
        fields = '__all__'
        widgets = {
            'description': WysiwygWidget(),
            'bio': WysiwygWidget(),
        }


# ============================================================================
# INLINE ADMINS
# ============================================================================

class MonthHeroInline(TabularInline):
    """Inline for heroes in Month admin"""
    model = MonthHero
    extra = 1
    fields = ['user', 'type', 'image', 'is_active']
    autocomplete_fields = ['user']
    classes = ['collapse']


class MentorInline(TabularInline):
    """Inline for mentors in Direction admin"""
    model = Mentor
    extra = 0
    fields = ['full_name', 'image', 'is_active']
    readonly_fields = ['full_name']
    classes = ['collapse']


# ============================================================================
# MAIN ADMIN CLASSES
# ============================================================================
@admin.register(Month)
class MonthAdmin(ImportExportModelAdmin, ModelAdmin):
    """Advanced admin for Month model"""
    form = MonthAdminForm
    list_display = [
        'name',
        'hero_count',
        'student_hero_count',
        'teacher_hero_count',
        'is_active_badge',
        'created_at_formatted'
    ]
    list_filter = [
        'is_active',
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    inlines = [MonthHeroInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'is_active'),
            'classes': ['tab'],
        }),
        (_('Details'), {
            'fields': ('description',),
            'classes': ['tab'],
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['created_at']

    actions = ['activate_months', 'deactivate_months']

    # Custom display methods
    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Total Heroes"), ordering="hero_count")
    def hero_count(self, obj):
        count = obj.heroes.count()
        if count > 0:
            url = reverse('admin:core_monthhero_changelist') + f'?month__id__exact={obj.id}'
            return format_html('<a href="{}">{} Heroes</a>', url, count)
        return count

    @display(description=_("Students"), ordering="student_count")
    def student_hero_count(self, obj):
        count = obj.heroes.filter(type='student').count()
        return format_html('<span style="color: #10b981;">{}</span>', count)

    @display(description=_("Teachers"), ordering="teacher_count")
    def teacher_hero_count(self, obj):
        count = obj.heroes.filter(type='teacher').count()
        return format_html('<span style="color: #3b82f6;">{}</span>', count)

    @display(description=_("Created"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")

    # Custom queryset with annotations
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            hero_count=Count('heroes'),
            student_count=Count('heroes', filter=Q(heroes__type='student')),
            teacher_count=Count('heroes', filter=Q(heroes__type='teacher'))
        )

    # Custom actions
    @admin.action(description=_("Activate selected months"))
    def activate_months(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} months activated successfully.")

    @admin.action(description=_("Deactivate selected months"))
    def deactivate_months(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} months deactivated successfully.")

@admin.register(MonthHero)
class MonthHeroAdmin(ImportExportModelAdmin, ModelAdmin):
    """Advanced admin for MonthHero model"""
    list_display = [
        'image_thumbnail',
        'user_info',
        'month_info',
        'type_badge',
        'is_active_badge',
        'created_at_formatted'
    ]
    list_filter = [
        ('type', MultipleChoicesDropdownFilter),
        'is_active',
        'month',
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'month__name',
        'description'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['user', 'month']

    fieldsets = (
        (_('Hero Information'), {
            'fields': ('month', 'user', 'type'),
            'classes': ['tab'],
        }),
        (_('Media'), {
            'fields': ('image', 'image_preview'),
            'classes': ['tab'],
        }),
        (_('Description'), {
            'fields': ('description', 'is_active'),
            'classes': ['tab'],
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['image_preview', 'created_at']

    actions = ['activate_heroes', 'deactivate_heroes', 'change_to_student', 'change_to_teacher']

    # Custom display methods
    @display(description=_("Image"))
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No image</span>')

    @display(description=_("User"), ordering="user__username")
    def user_info(self, obj):
        full_name = obj.user.get_full_name() or obj.user.username
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, full_name)

    @display(description=_("Month"), ordering="month__name")
    def month_info(self, obj):
        url = reverse('admin:core_month_change', args=[obj.month.id])
        return format_html('<a href="{}">{}</a>', url, obj.month.name)

    @display(description=_("Type"), label=True)
    def type_badge(self, obj):
        return obj.type == 'student', obj.get_type_display()

    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Created"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y %H:%M")

    @display(description=_("Image Preview"))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return _("No image uploaded")

    # Custom actions
    @admin.action(description=_("Activate selected heroes"))
    def activate_heroes(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} heroes activated.")

    @admin.action(description=_("Deactivate selected heroes"))
    def deactivate_heroes(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} heroes deactivated.")

    @admin.action(description=_("Change type to Student"))
    def change_to_student(self, request, queryset):
        updated = queryset.update(type='student')
        self.message_user(request, f"{updated} heroes changed to Student.")

    @admin.action(description=_("Change type to Teacher"))
    def change_to_teacher(self, request, queryset):
        updated = queryset.update(type='teacher')
        self.message_user(request, f"{updated} heroes changed to Teacher.")

@admin.register(Direction)
class DirectionAdmin(ImportExportModelAdmin, ModelAdmin):
    """Advanced admin for Direction model"""
    list_display = [
        'title',
        'mentor_count',
        'active_mentor_count',
        'is_active_badge',
        'created_at_formatted'
    ]
    list_filter = [
        'is_active',
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ['title', 'description']
    ordering = ['title']
    date_hierarchy = 'created_at'
    inlines = [MentorInline]

    fieldsets = (
        (_('Direction Information'), {
            'fields': ('title', 'is_active'),
            'classes': ['tab'],
        }),
        (_('Description'), {
            'fields': ('description',),
            'classes': ['tab'],
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['created_at']
    actions = ['activate_directions', 'deactivate_directions']

    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Total Mentors"), ordering="total_mentors")
    def mentor_count(self, obj):
        count = obj.mentors.count()
        if count > 0:
            url = reverse('admin:core_mentor_changelist') + f'?direction__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count

    @display(description=_("Active Mentors"), ordering="active_mentors")
    def active_mentor_count(self, obj):
        count = obj.mentors.filter(is_active=True).count()
        return format_html('<span style="color: #10b981;">{}</span>', count)

    @display(description=_("Created"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_mentors=Count('mentors'),
            active_mentors=Count('mentors', filter=Q(mentors__is_active=True))
        )

    @admin.action(description=_("Activate selected directions"))
    def activate_directions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} directions activated.")

    @admin.action(description=_("Deactivate selected directions"))
    def deactivate_directions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} directions deactivated.")

@admin.register(Mentor)
class MentorAdmin(ImportExportModelAdmin, ModelAdmin):
    """Advanced admin for Mentor model"""
    form = MentorAdminForm
    list_display = [
        'image_thumbnail',
        'full_name',
        'direction_info',
        'is_active_badge',
        'created_at_formatted'
    ]
    list_filter = [
        'is_active',
        'direction',
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ['full_name', 'description', 'bio']
    ordering = ['full_name']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['direction']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('full_name', 'direction', 'is_active'),
            'classes': ['tab'],
        }),
        (_('Media'), {
            'fields': ('image', 'image_preview'),
            'classes': ['tab'],
        }),
        (_('About'), {
            'fields': ('description', 'bio'),
            'classes': ['tab'],
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['image_preview', 'created_at']
    actions = ['activate_mentors', 'deactivate_mentors']

    @display(description=_("Photo"))
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No photo</span>')

    @display(description=_("Direction"), ordering="direction__title")
    def direction_info(self, obj):
        if obj.direction:
            url = reverse('admin:core_direction_change', args=[obj.direction.id])
            return format_html('<a href="{}">{}</a>', url, obj.direction.title)
        return format_html('<span style="color: #9ca3af;">No direction</span>')

    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Created"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")

    @display(description=_("Photo Preview"))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return _("No photo uploaded")

    @admin.action(description=_("Activate selected mentors"))
    def activate_mentors(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} mentors activated.")

    @admin.action(description=_("Deactivate selected mentors"))
    def deactivate_mentors(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} mentors deactivated.")

@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, ModelAdmin):
    """Advanced admin for News model"""
    form = NewsAdminForm
    list_display = [
        'image_thumbnail',
        'title_with_link',
        'content_preview',
        'is_active_badge',
        'created_at_formatted'
    ]
    list_filter = [
        'is_active',
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('News Information'), {
            'fields': ('title', 'is_active'),
            'classes': ['tab'],
        }),
        (_('Content'), {
            'fields': ('content',),
            'classes': ['tab'],
        }),
        (_('Media'), {
            'fields': ('image', 'image_preview'),
            'classes': ['tab'],
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['image_preview', 'created_at']
    actions = ['activate_news', 'deactivate_news', 'duplicate_news']

    @display(description=_("Image"))
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No image</span>')

    @display(description=_("Title"), ordering="title")
    def title_with_link(self, obj):
        return format_html('<strong>{}</strong>', obj.title)

    @display(description=_("Preview"))
    def content_preview(self, obj):
        preview = obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
        return format_html('<span style="color: #6b7280;">{}</span>', preview)

    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Published"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y %H:%M")

    @display(description=_("Image Preview"))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 600px; max-height: 400px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return _("No image uploaded")

    @admin.action(description=_("Activate selected news"))
    def activate_news(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} news articles activated.")

    @admin.action(description=_("Deactivate selected news"))
    def deactivate_news(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} news articles deactivated.")

    @admin.action(description=_("Duplicate selected news"))
    def duplicate_news(self, request, queryset):
        for news in queryset:
            news.pk = None
            news.title = f"{news.title} (Copy)"
            news.save()
        self.message_user(request, f"{queryset.count()} news articles duplicated.")


# ============================================================================
# CUSTOM USER ADMIN
# ============================================================================
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    """Enhanced User admin with Unfold styling"""
    list_display = [
        'username',
        'email',
        'full_name_display',
        'is_staff_badge',
        'is_active_badge',
        'hero_count',
        'date_joined_formatted'
    ]
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        ('date_joined', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']
    date_hierarchy = 'date_joined'

    fieldsets = (
        (_('User Information'), {
            'fields': ('username', 'password'),
            'classes': ['tab'],
        }),
        (_('Personal Information'), {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ['tab'],
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ['tab'],
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ['tab'],
        }),
    )

    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ['groups', 'user_permissions']

    @display(description=_("Full Name"))
    def full_name_display(self, obj):
        full_name = obj.get_full_name()
        return full_name if full_name else format_html('<span style="color: #9ca3af;">Not set</span>')

    @display(description=_("Staff"), label=True)
    def is_staff_badge(self, obj):
        return obj.is_staff, _("Staff") if obj.is_staff else _("User")

    @display(description=_("Status"), label=True)
    def is_active_badge(self, obj):
        return obj.is_active, _("Active") if obj.is_active else _("Inactive")

    @display(description=_("Hero Awards"), ordering="hero_count")
    def hero_count(self, obj):
        count = obj.month_heroes.count()
        if count > 0:
            url = reverse('admin:core_monthhero_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} 🏆</a>', url, count)
        return count

    @display(description=_("Joined"), ordering="date_joined")
    def date_joined_formatted(self, obj):
        return obj.date_joined.strftime("%b %d, %Y")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(hero_count=Count('month_heroes'))


# ============================================================================
# CUSTOM GROUP ADMIN
# ============================================================================
admin.site.unregister(Group)
@admin.register(Group)
class CustomGroupAdmin(ModelAdmin):
    """Enhanced Group admin with Unfold styling"""
    list_display = ['name', 'user_count', 'permission_count']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ['permissions']

    @display(description=_("Users"))
    def user_count(self, obj):
        count = obj.user_set.count()
        if count > 0:
            url = reverse('admin:auth_user_changelist') + f'?groups__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count

    @display(description=_("Permissions"))
    def permission_count(self, obj):
        return obj.permissions.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            user_count=Count('user'),
            permission_count=Count('permissions')
        )