from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import AuthViewSet

router_v1 = DefaultRouter()

router_v1.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
