from rest_framework import serializers
from drf_user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    UserRegisterSerializer is a model serializer which includes the
    attributes that are required for registering a user.
    """

    class Meta:
        """Passing model metadata"""

        model = User
        fields = (
            "id",
            "username",
            "email",
            "mobile",
            "password",
            "is_superuser",
            "is_staff",
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}
