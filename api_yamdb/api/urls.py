from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegistrationAPIView, GettingTokenAPIView


router = DefaultRouter()

router.register('v1/users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', GettingTokenAPIView.as_view()),
]