from .models import BrownBag, Hangout, SecretSanta, Profile
from .serializers import UserSerializer, ProfileSerializer, \
    BrownbagSerializer, HangoutSerializer, SecretSantaSerializer
from rest_framework import generics,
from django.contrib.auth.models import User


class UserView(generics.ListCreateAPIView):
    """A concrete view for creating new users and listing them."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateHangout(generics.ListCreateAPIView):
    """A concrete view for creating new hangouts and listing them."""
    queryset = Hangout.objects.all()
    serializer_class = HangoutSerializer


class CreateBrownbag(generics.ListCreateAPIView):
    """A concrete view for creating new BrownBags and listing them."""
    queryset = BrownBag.objects.all()
    serializer_class = BrownbagSerializer


class CreateSecretSanta(generics.ListCreateAPIView):
    """A concrete view for creating new SecretSantas and listing them."""
    queryset = SecretSanta.objects.all()
    serializer_class = SecretSantaSerializer
