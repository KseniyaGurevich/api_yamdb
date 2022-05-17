from django.urls import path, include
from rest_framework import routers
from api.views import (CommentViewsSet, ReviewViewsSet, UserViewSet,
                       RegistrationAPIView, GettingTokenAPIView,
                       GenreViewSet, CategoryViewSet)


router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewsSet,
                basename='reviews'
                )

router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments/',
                CommentViewsSet,
                basename='comments'
                )
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', GettingTokenAPIView.as_view()),
]
