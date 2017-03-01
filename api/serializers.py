from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, BrownBag, SecretSanta, Hangout


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
        ordered_dict_profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        profile = dict(ordered_dict_profile)

        for field in profile:
            # set profile photo, bio and date of birth
            setattr(user.profile, field, profile[field])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update an existing user and their corresponding profile."""
        ordered_dict_profile = validated_data.pop('profile')
        for field in validated_data:
            if User._meta.get_field(field):
                setattr(instance, field, validated_data[field])
        profile = dict(ordered_dict_profile)

        for field in profile:
            setattr(instance.profile, field, profile[field])

        instance.save()
        return instance


class BrownbagSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the BrownBag model."""

    class Meta:

        model = BrownBag
        fields = ('id', 'date', 'status', 'user')


class HangoutSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the Hangout model."""

    # members = UserSerializer(many=True)

    class Meta:

        model = Hangout
        fields = ('id', 'date', 'members')


class SecretSantaSerializer(serializers.ModelSerializer):
    """This class defines a serializer for the SecretSanta model."""

    class Meta:

        model = SecretSanta
        fields = ('id', 'date', 'santa', 'giftee')
