from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from requests import Response
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import User
from .serializers import (UserSerializer, RegistrationSerializer,
                          GettingTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get("username")
            user = get_object_or_404(
                User,
                username=username
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код активации',
                f'Password для {username}: {confirmation_code}',
                'host@gmail.com',
                [email],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[IsAuthenticated]
            )
    def my_profile(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

    @action(detail=False, methods=['get', 'patch', 'delete'],
            url_path=r'(?P<username>[\w.@+-]+)')
    def username_profile(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        if request.method == 'DELETE':
            user.delete()


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get("username")
            user = get_object_or_404(
                User,
                username=username
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код активации',
                f'Password для {username}: {confirmation_code}',
                'host@gmail.com',
                [email],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GettingTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GettingTokenSerializer

    def post(self, request):
        serializer = GettingTokenSerializer(data=request.data)
        if serializer.is_valid():
            #confirmation_code = request.data.get('confirmation_code')
            #username = request.data.get('username')
            username = serializer.validated_data.get("username")
            confirmation_code = serializer.validated_data.get("confirmation_code")
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"token": str(refresh.access_token)},
                    status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


