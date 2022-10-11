from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.Serializer):
    # read_only fields
    id = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    # write_only fields
    password = serializers.CharField(max_length=50, write_only=True)

    # mandatory_fields
    username = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="This username is already in use"
            )
        ],
    )
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="This email is already in use"
            )
        ],
    )
    birthdate = serializers.DateField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    # optional fields
    bio = serializers.CharField(allow_null=True, allow_blank=True, default="")
    is_critic = serializers.BooleanField(default=True)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)

        return new_user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
