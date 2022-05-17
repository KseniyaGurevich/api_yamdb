from django.db.models import Avg
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin, IsAdminOrReadOnly
from api.serializers import (CommentSerializer, ReviewSerializer,
                             UserSerializer, RegistrationSerializer,
                             GettingTokenSerializer, UserEditSerializer,
                             GenreSerializer, CategorySerializer)

from reviews.models import Review, Title, Genre, Category
from reviews.permissions import IsOwnerAdminModeratorOrReadOnly

from users.models import User


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>[-\w]+)',
            permission_classes=(IsAdmin,)
            )
    def slug(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>[-\w]+)',
            permission_classes=(IsAdmin,)
            )
    def slug(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        score=Avg("reviews__score")).order_by("name")


class CommentViewsSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewsSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=(IsAuthenticated,),
            serializer_class=UserEditSerializer,
            )
    def my_profile(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if request.data.get('username') in (
                User.objects.values_list('username', flat=True)
        ):
            user = get_object_or_404(
                User, username=request.data.get('username')
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код активации',
                f'Password для {user.username}: {confirmation_code}',
                'host@gmail.com',
                [user.email],
                fail_silently=False
            )
            serializer.is_valid(raise_exception=True)
            return Response(status)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get("username")
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код активации',
                f'Password для {username}: {confirmation_code}',
                'host@gmail.com',
                [email],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class GettingTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GettingTokenSerializer

    def post(self, request):
        serializer = GettingTokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = request.data.get('confirmation_code')
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"token": str(refresh.access_token)},
                    status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
