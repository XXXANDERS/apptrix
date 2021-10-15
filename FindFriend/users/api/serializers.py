from io import StringIO

from rest_framework import serializers
# from rest_framework.validators import
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from users.models import CustomUser


class ClientsSerializer(serializers.ModelSerializer):
    # password = serializers.HiddenField()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'avatar', 'sex')


class ClientsCreateSerializer(serializers.ModelSerializer):
    # serializers.CharField(allow_blank=False)

    class Meta:
        model = CustomUser
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': True},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar', 'sex')  # there what you want to initial.

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль слишком короткий")
        return value

    def create(self, validated_data):
        client = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
            sex=validated_data.get('sex'),
        )

        client.set_password(validated_data['password'])
        client.save()

        return client
