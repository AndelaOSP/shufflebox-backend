from .models import BrownBag, Hangout, SecretSanta, Profile
from .serializers import UserSerializer, ProfileSerializer, \
    BrownbagSerializer, HangoutSerializer, SecretSantaSerializer
from rest_framework import generics,
from django.contrib.auth.models import User


class UserView(generics.ListAPIView):
    """This class creates a concrete view for listing current users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
