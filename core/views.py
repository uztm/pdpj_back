from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from .models import Month, MonthHero, Mentor, Direction, News
from .serializers import (
    MonthSerializer, MonthHeroSerializer,
    MentorSerializer, DirectionSerializer, NewsSerializer
)


class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get']


class MonthViewSet(ReadOnlyViewSet):
    queryset = Month.objects.all().order_by('-created_at')
    serializer_class = MonthSerializer


class MonthHeroViewSet(ReadOnlyViewSet):
    queryset = MonthHero.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = MonthHeroSerializer


class MentorViewSet(ReadOnlyViewSet):
    queryset = Mentor.objects.filter(is_active=True).order_by('full_name')
    serializer_class = MentorSerializer


class DirectionViewSet(ReadOnlyViewSet):
    queryset = Direction.objects.filter(is_active=True).order_by('title')
    serializer_class = DirectionSerializer


class NewsViewSet(ReadOnlyViewSet):
    queryset = News.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = NewsSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'months': reverse('month-list', request=request, format=format),
        'heroes': reverse('hero-list', request=request, format=format),
        'mentors': reverse('mentor-list', request=request, format=format),
        'directions': reverse('direction-list', request=request, format=format),
        'news': reverse('news-list', request=request, format=format),
    })
