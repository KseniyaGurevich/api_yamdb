from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.core.mail import send_mail

from users.models import User
from .serializers import (UserSerializer, RegistrationSerializer, GettingTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.filter(username=request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.user
        email = request.data['email']
        serializer = RegistrationSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                f'confirmation_code: {user.token}',
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GettingTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GettingTokenSerializer

    def post(self, request):
        user = request.user
        serializer = GettingTokenSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


