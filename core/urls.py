from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MonthViewSet, MonthHeroViewSet,
    MentorViewSet, DirectionViewSet, NewsViewSet, api_root
)

router = DefaultRouter()
router.register(r'months', MonthViewSet, basename='month')
router.register(r'heroes', MonthHeroViewSet, basename='hero')
router.register(r'mentors', MentorViewSet, basename='mentor')
router.register(r'directions', DirectionViewSet, basename='direction')
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]
