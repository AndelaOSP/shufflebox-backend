from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, BrownBag, SecretSanta, Hangout, UserHangout


class ProfileSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the Profile model."""

    class Meta:

        model = Profile
        fields = ('avatar', 'birth_date', 'bio')


class UserSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the User model."""

    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:

        model = User
        fields = ('id', 'username', 'email', 'profile')

    def create(self, validated_data):
        """Create and returns a new user."""
        user = User.objects.create_user(**validated_data)
        return user


class BrownbagSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the BrownBag model."""

    class Meta:

        model = BrownBag
        fields = ('id', 'date', 'status', 'user_id')
        read_only_fields = ('date')


class HangoutSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the Hangout model."""

    class Meta:

        model = Hangout
        fields = ('id', 'date', 'members')


class SecretSantaSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the SecretSanta model."""

    class Meta:

        model = SecretSanta
        fields = ('id', 'date', 'santa', 'giftee')
        read_only_fields = ('date')
