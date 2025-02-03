from rest_framework import serializers
from apps.user.models import User


class UserForgotPassword(serializers.ModelSerializer):
    user_email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['user_email   ']