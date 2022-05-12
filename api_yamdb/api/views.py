from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from api.serializers import CommentSerializer, ReviewSerializer

from reviews.models import Review, Title
from reviews.permissions import IsOwnerAdminModeratorOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        score=Avg("reviews__score")).order_by("name")


class CommentViewsSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = IsOwnerAdminModeratorOrReadOnly

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewsSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = IsOwnerAdminModeratorOrReadOnly

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
