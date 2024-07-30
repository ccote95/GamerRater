from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views.users import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
]

