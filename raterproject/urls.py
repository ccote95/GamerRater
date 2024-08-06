from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views.users import UserViewSet
from raterapi.views import GameView,register_user, login_user,CategoryView,GameReview

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r"games", GameView, basename='game')
router.register(r'categories', CategoryView, basename='category')
router.register(r'reviews', GameReview, basename='review')
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
]

