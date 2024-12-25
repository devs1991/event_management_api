from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        """Ensure the username is unique and contains only alphanumeric characters."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not value.isalnum():
            raise serializers.ValidationError("Username must contain only alphanumeric characters.")
        return value

    def validate_email(self, value):
        """Ensure the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_role(self, value):
        """Ensure the role is valid."""
        valid_roles = ['admin', 'event_organizer', 'attendee']
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of {valid_roles}.")
        return value

    def create(self, validated_data):
        """Hash the password when creating a user."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
