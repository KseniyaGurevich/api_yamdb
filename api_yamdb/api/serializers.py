from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class GettingTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    token = serializers.CharField(read_only=True,)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')
        read_only_fields = ('token',)
