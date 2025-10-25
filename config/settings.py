"""
Django settings for config project with Advanced Unfold Admin Integration.
"""

from pathlib import Path
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5==2xp941gcg-p+indhieqs29ap+e74flr=3ws)eirw&k0mix%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'api.pdpjunior.uz',
    'www.api.pdpjunior.uz',
    'localhost',
    '127.0.0.1',
    '94.158.49.59',
]


CSRF_TRUSTED_ORIGINS = [
    'https://api.pdpjunior.uz',
    'https://www.api.pdpjunior.uz',
    'http://api.pdpjunior.uz',
    'http://www.api.pdpjunior.uz',
]

CORS_ALLOW_CREDENTIALS = True


# Application definition
INSTALLED_APPS = [
    # Unfold Admin - MUST be before django.contrib.admin
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    'unfold.contrib.guardian',
    'unfold.contrib.simple_history',

    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'rest_framework',
    'corsheaders',
    'import_export',
    'django_filters',

    # Local Apps
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================================
# UNFOLD ADMIN ADVANCED CONFIGURATION
# ============================================================================

def environment_callback(request):
    """Return environment badge for admin header"""
    if DEBUG:
        return ["Development", "warning"]
    return ["Production", "success"]


def badge_callback(request):
    """Custom badge in admin header"""
    return 3  # Number of pending items/notifications


def dashboard_callback(request, context):
    """Add custom data to admin dashboard"""
    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import timedelta
    from core.models import Month, MonthHero, Mentor, Direction, News

    # Calculate statistics
    today = timezone.now()
    last_month = today - timedelta(days=30)

    context.update({
        "navigation": [
            {
                "title": _("Quick Stats"),
                "items": [
                    {
                        "title": _("Total Months"),
                        "value": Month.objects.count(),
                        "description": _("All time"),
                    },
                    {
                        "title": _("Active Heroes"),
                        "value": MonthHero.objects.filter(is_active=True).count(),
                        "description": _("Currently active"),
                    },
                    {
                        "title": _("Mentors"),
                        "value": Mentor.objects.filter(is_active=True).count(),
                        "description": _("Teaching now"),
                    },
                    {
                        "title": _("News Articles"),
                        "value": News.objects.filter(is_active=True).count(),
                        "description": _("Published"),
                    },
                ],
            },
            {
                "title": _("Recent Activity"),
                "items": [
                    {
                        "title": _("New Heroes"),
                        "value": MonthHero.objects.filter(created_at__gte=last_month).count(),
                        "description": _("Last 30 days"),
                    },
                    {
                        "title": _("New News"),
                        "value": News.objects.filter(created_at__gte=last_month).count(),
                        "description": _("Last 30 days"),
                    },
                    {
                        "title": _("Active Directions"),
                        "value": Direction.objects.filter(is_active=True).count(),
                        "description": _("Available courses"),
                    },
                ],
            },
        ],
        "kpi": [
            {
                "title": "Student Heroes",
                "metric": MonthHero.objects.filter(type='student', is_active=True).count(),
            },
            {
                "title": "Teacher Heroes",
                "metric": MonthHero.objects.filter(type='teacher', is_active=True).count(),
            },
        ],
    })
    return context


UNFOLD = {
    "SITE_TITLE": "PDP Junior Admin",
    "SITE_HEADER": "PDP Junior Administration",
    "SITE_URL": "/",
    "SITE_ICON": None,

    # Branding
    "SITE_LOGO": None,
    "SITE_SYMBOL": "school",  # Material icon
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],

    # Display settings
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,

    # Callbacks
    "ENVIRONMENT": environment_callback,  # ✅ no quotes
    "DASHBOARD_CALLBACK": dashboard_callback,  # ✅ no quotes
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },

    # Theming
    "THEME": "dark",  # "light" or "dark"
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "129 140 248",
            "500": "99 102 241",
            "600": "79 70 229",
            "700": "67 56 202",
            "800": "55 48 163",
            "900": "49 46 129",
            "950": "30 27 75",
        },
    },

    # Custom CSS/JS
    "STYLES": [
        lambda request: static("css/custom-admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/custom-admin.js"),
    ],

    # Sidebar configuration
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Dashboard"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "badge": badge_callback,
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("API Documentation"),
                        "icon": "api",
                        "link": "/api/",
                        "badge": "New",
                    },
                ],
            },
            {
                "title": _("Content Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Months"),
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:core_month_changelist"),
                        "permission": lambda request: request.user.has_perm("core.view_month"),
                    },
                    {
                        "title": _("Month Heroes"),
                        "icon": "stars",
                        "link": reverse_lazy("admin:core_monthhero_changelist"),
                        "permission": lambda request: request.user.has_perm("core.view_monthhero"),
                    },
                    {
                        "title": _("News & Articles"),
                        "icon": "article",
                        "link": reverse_lazy("admin:core_news_changelist"),
                        "permission": lambda request: request.user.has_perm("core.view_news"),
                    },
                ],
            },
            {
                "title": _("Educational"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Directions"),
                        "icon": "explore",
                        "link": reverse_lazy("admin:core_direction_changelist"),
                        "permission": lambda request: request.user.has_perm("core.view_direction"),
                    },
                    {
                        "title": _("Mentors"),
                        "icon": "school",
                        "link": reverse_lazy("admin:core_mentor_changelist"),
                        "permission": lambda request: request.user.has_perm("core.view_mentor"),
                    },
                ],
            },
            {
                "title": _("User Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_user"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_group"),
                    },
                ],
            },
            {
                "title": _("System"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Settings"),
                        "icon": "settings",
                        "link": "#",
                    },
                    {
                        "title": _("Logs"),
                        "icon": "description",
                        "link": "#",
                    },
                ],
            },
        ],
    },

    # Tabs configuration for model detail pages
    "TABS": [
    {
        "models": [
            "core.month",
        ],
        "items": [
            {
                "title": _("Basic Info"),
                "link": reverse_lazy("admin:core_month_changelist"),
                "permission": lambda request: request.user.has_perm("core.view_month"),  # ✅ to‘g‘ri
            },
            {
                "title": _("Heroes"),
                "link": reverse_lazy("admin:core_monthhero_changelist"),
                "permission": lambda request: request.user.has_perm("core.view_monthhero"),  # ✅ to‘g‘ri
            },
        ],
    },
    {
        "models": [
            "core.direction",
        ],
        "items": [
            {
                "title": _("Directions"),
                "link": reverse_lazy("admin:core_direction_changelist"),
                "permission": lambda request: request.user.has_perm("core.view_direction"),
            },
            {
                "title": _("Mentors"),
                "link": reverse_lazy("admin:core_mentor_changelist"),
                "permission": lambda request: request.user.has_perm("core.view_mentor"),
            },
        ],
    },
]

}