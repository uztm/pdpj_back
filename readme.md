# Django API Setup Guide

## Changes Made

1. **Added image field to MonthHero model** with custom upload path
2. **Fixed serializers** to match actual model fields
3. **Removed authentication requirements** - all GET endpoints are now public
4. **Custom image path format**: `/media/users/YYYYMMDD_username.ext`

## Step-by-Step Setup

### 1. Update Your Files

Replace the following files with the updated versions:
- `core/models.py`
- `core/serializers.py`
- `core/admin.py`
- `config/settings.py`

### 2. Create and Run Migrations

```bash
# Create migration for the new image field
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 3. Create Media Directory

```bash
# Create media directories
mkdir -p media/users
mkdir -p media/mentors
mkdir -p media/news
```

### 4. Test the API

Start the development server:
```bash
python manage.py runserver
```

## API Endpoints (All Public - No Auth Required)

- `GET /api/` - API root with all available endpoints
- `GET /api/months/` - List all months
- `GET /api/months/{id}/` - Get specific month with heroes
- `GET /api/heroes/` - List all month heroes
- `GET /api/heroes/{id}/` - Get specific hero
- `GET /api/mentors/` - List all mentors
- `GET /api/mentors/{id}/` - Get specific mentor
- `GET /api/directions/` - List all directions with mentors
- `GET /api/directions/{id}/` - Get specific direction
- `GET /api/news/` - List all news
- `GET /api/news/{id}/` - Get specific news item

## Image Upload Format

When creating a MonthHero through Django admin:
1. Upload an image
2. The system automatically saves it as: `/media/users/YYYYMMDD_username.ext`
3. In API responses, the image URL will be: `/media/users/YYYYMMDD_username.jpg`

### Example Response

```json
{
  "id": 1,
  "month": 1,
  "month_name": "January 2025",
  "user": {
    "id": 2,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "type": "student",
  "image": "/media/users/20251007_john_doe.jpg",
  "description": "Outstanding performance in Python programming",
  "is_active": true,
  "created_at": "2025-10-07T10:30:00Z"
}
```

## Creating Test Data

### Via Django Admin

1. Access admin panel: `http://localhost:8000/admin/`
2. Create a superuser if needed:
   ```bash
   python manage.py createsuperuser
   ```
3. Add Months, Users, Directions, Mentors, News, and MonthHeroes

### Via Django Shell

```python
python manage.py shell

from django.contrib.auth.models import User
from core.models import Month, MonthHero, Direction, Mentor, News

# Create a month
month = Month.objects.create(name="January 2025", is_active=True)

# Create a user
user = User.objects.create_user(username="john_doe", email="john@example.com")

# Create a month hero (upload image through admin)
hero = MonthHero.objects.create(
    month=month,
    user=user,
    type="student",
    description="Outstanding student"
)

# Create a direction
direction = Direction.objects.create(title="Backend Development")

# Create a mentor
mentor = Mentor.objects.create(
    full_name="Jane Smith",
    direction=direction,
    description="Senior Backend Developer"
)

# Create news
news = News.objects.create(
    title="New Course Launch",
    content="We are launching a new Python course..."
)
```

## Important Notes

1. **No Authentication Required**: All GET endpoints are public
2. **Image Storage**: Images are stored in `media/users/` with date+username format
3. **CORS Enabled**: All origins are allowed (for development)
4. **Pagination**: Responses are paginated (10 items per page)
5. **Active Filter**: Only active items are returned (except Months which return all)

## Troubleshooting

### Media files not showing?
Make sure `MEDIA_ROOT` directory exists and check URL configuration in `config/urls.py`

### Migration errors?
Delete `db.sqlite3` and all migration files except `__init__.py`, then run migrations again

### Image not uploading?
Ensure `Pillow` is installed: `pip install Pillow`