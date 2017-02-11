from .models import BrownBag, Hangout, SecretSanta, Profile
from .serializers import UserSerializer, ProfileSerializer, \
    BrownbagSerializer, HangoutSerializer, SecretSantaSerializer
from rest_framework import generics,
from django.contrib.auth.models import User


class UserView(generics.ListCreateAPIView):
    """A view for creating new users and listing them."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HangoutView(generics.ListCreateAPIView):
    """A view for creating new hangouts and listing them."""
    queryset = Hangout.objects.all()
    serializer_class = HangoutSerializer


class HangoutDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a hangout instance."""
    queryset = Hangout.objects.all()
    serializer_class = HangoutSerializer


class BrownbagView(generics.ListCreateAPIView):
    """A view for creating new BrownBags and listing them."""
    queryset = BrownBag.objects.all()
    serializer_class = BrownbagSerializer


class BrownbagDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a brownbag instance."""
    queryset = BrownBag.objects.all()
    serializer_class = BrownbagSerializer


class SecretSantaView(generics.ListCreateAPIView):
    """A view for creating a new SecretSanta pair and listing all pairs."""
    queryset = SecretSanta.objects.all()
    serializer_class = SecretSantaSerializer
