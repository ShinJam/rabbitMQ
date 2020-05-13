from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Login

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = "auth"
urlpatterns = [
    path('login/', Login.as_view()),
] + router.urls