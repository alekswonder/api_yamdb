from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('v1/', include(router.urls)),
]
