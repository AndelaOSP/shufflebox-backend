from .models import BrownBag, Hangout, SecretSanta, Profile
from .serializers import UserSerializer, ProfileSerializer, \
    BrownbagSerializer, HangoutSerializer, SecretSantaSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import User
from datetime import datetime


class UserView(generics.ListCreateAPIView):
    """A view for creating new users and listing them."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ShuffleView(APIView):
    """A view for handling shuffling requests from consumption clients."""

    def post(self, request):
        """
        Return a query set according to the post message status.
        """
        try:
            request_type = request.data['type']
            if request_type == "brownbag":
                # Create the next brownbag
                # dummy data simulated from the shufflebox module
                data = {
                    "date": str(datetime.now().date()),
                    "status": "nextInLine",
                    "user_id": 1
                }
                serializer = BrownbagSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request_type == "hangout":
                # Create hangout groups for the month
                # dummy data simulated from the shufflebox module
                data = {
                    "date": str(datetime.now().date()),
                    "members": [1, 2]
                }
                serializer = HangoutSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request_type == "secretsanta":
                # Create all secretsanta pairs for that year
                # dummy data simulated from the shufflebox module
                data = {
                    "date": str(datetime.now().date()),
                    "santa": 2,
                    "giftee": 1
                }
                serializer = SecretSantaSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    "Bad Request With Wrong Unexpected Value of 'type' key",
                    status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(
                "Bad Request: Missing Key 'type'",
                status=status.HTTP_400_BAD_REQUEST)


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
