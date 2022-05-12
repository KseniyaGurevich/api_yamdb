from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import (UserSerializer, RegistrationSerializer, GettingTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'patch'], name='me')
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = request.data['email']
            username = request.data['username']
            user = request.user
            user.last_login = None
            user.password = ''
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
        username = request.data['username']
        print('*' * 30)
        print(username)
        print('*' * 30)
        serializer = GettingTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            confirmation_code = request.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            refresh = RefreshToken.for_user(user)
            token = refresh.access_token
            if default_token_generator.check_token(user, confirmation_code):
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


