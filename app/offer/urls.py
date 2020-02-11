from django.urls import path, include
from rest_framework.routers import DefaultRouter

from offer import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'offer'

urlpatterns = [
    path('', include(router.urls))
]
