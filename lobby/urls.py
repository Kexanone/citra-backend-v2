from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet

router = DefaultRouter(trailing_slash = False)
# Temporary fix for older Citra versions
# Allow POST to be used as PATCH
router.routes[2].mapping['post'] = 'partial_update'
router.register(__package__, RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
