from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
]
