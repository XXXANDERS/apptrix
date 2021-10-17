from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser, UserMatch


class UsersSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'avatar', 'sex')
        # fields = ('email', 'first_name', 'last_name', 'avatar', 'sex')

    def get_sex(self, obj):
        return obj.get_sex_display()


class UsersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': True},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'sex': {'required': True, 'allow_blank': False},
        }
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar', 'sex')  # there what you want to initial.

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль слишком короткий")
        return value

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
            sex=validated_data.get('sex'),
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UsersMatchSerializer(serializers.ModelSerializer):
    from_user = UsersSerializer(many=False)
    for_user = UsersSerializer(many=False)

    class Meta:
        model = UserMatch
        fields = ('from_user', 'for_user', 'like',)
        depth = 1


class UsersMatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatch
        fields = ('from_user', 'for_user', 'like',)
        read_only_fields = ('from_user', 'for_user')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserMatch.objects.all(),
        #         fields=['from_user', 'for_user']
        #     )
        # ]
