from django.urls import path, include
from rest_framework import routers
from api.views import CommentViewsSet, ReviewViewsSet


router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                ReviewViewsSet,
                basename='reviews'
                )

router.register(r'titles/(?P<title_id>\d+)/reviews/)'
                r'/comments/',
                CommentViewsSet,
                basename='comments'
                )

urlpatterns = [
    path('v1/', include(router.urls)),
]