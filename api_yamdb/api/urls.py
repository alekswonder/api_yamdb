from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AuthViewSet, UserViewSet)

app_name = 'api'

router_api_v1 = DefaultRouter()

router_api_v1.register(r'auth', AuthViewSet, basename='auth')
router_api_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_api_v1.urls))
]
