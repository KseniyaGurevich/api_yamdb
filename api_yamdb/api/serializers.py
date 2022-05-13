from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',
                  'role', 'bio')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username'],
                message='User with exactly similar username и email exist'
            )
        ]

    def validate(self, data):
        if data['username'] == "me":
            raise serializers.ValidationError("Username can't be 'me'")
        return data


class GettingTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()
