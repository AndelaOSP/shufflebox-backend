from .models import Brownbag, Hangout, SecretSanta, Profile, Group
from .serializers import (
    UserSerializer, BrownbagSerializer, HangoutSerializer, SecretSantaSerializer
)
from .utils import SendMail, validate_address
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import User
from django.conf import settings
from shufflebox import Randomizer
from dateutil.relativedelta import relativedelta, FR

from rest_framework.renderers import JSONRenderer
from django.db import IntegrityError
from random import shuffle
import datetime
import calendar
import json
import functools

HANGOUT_GROUP_LIMIT = 10
SECRET_SANTA_LIMIT = 2


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
            request_type = request.data.get('type')
            size = request.data.get('limit', None)

            if request_type == "brownbag":
                try:
                    valid_number, users = check_people(int(size))
                    if not valid_number:
                        return Response(
                            {'message': "The number of people exceeds available users. Available users is {}".format(
                                users)},
                            status=status.HTTP_400_BAD_REQUEST)
                    check_date(datetime.date.today())
                    brownbag_data = create_brownbag(
                        datetime.date.today(), size)
                except IntegrityError:
                    # There exists a brownbag this Friday, create for next one
                    # Use latest friday as seed date to create next brownbag
                    latest_brownbag = Brownbag.objects.latest('date')
                    brownbag_data = create_brownbag(latest_brownbag.date, size)
                    data = serialize_brownbag(brownbag_data)
                    return Response(
                        data, status=status.HTTP_201_CREATED)
                except IndexError as e:
                    return Response(
                        {'error': e.args[0]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    return Response(
                        {'error': e.args}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = serialize_brownbag(brownbag_data)
                    return Response(
                        data, status=status.HTTP_201_CREATED)

            elif request_type == "hangout":
                # Create hangout groups for the month
                size = request.data.get('limit', HANGOUT_GROUP_LIMIT)
                try:
                    data = create_hangout(group_size=size)
                except IntegrityError:
                    return Response(
                        {'message': "Hangouts for this month already exists"},
                        status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response(
                        {'error': e}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data, status=status.HTTP_201_CREATED)

            elif request_type == "secretsanta":
                # Create all secretsanta pairs for that year
                users_queryset = User.objects.exclude(
                    email="shufflebox@andela.com" )
                users = list(users_queryset)
                shuffle(users)
                remainder = users[-1] and users.pop() if ((len(users) % 2) > 0) else None

                secret_santas = []

                santas = users[:len(users) // 2]
                giftees = users[len(users) // 2:]

                # Remove all existing secret santa pairs
                SecretSanta.objects.all().delete()

                # Santas to Giftees
                shuffle(giftees)
                for i in range(len(santas)):
                    secretsanta_pair = SecretSanta.objects.create(
                        date=str(datetime.datetime.now().date()),
                        santa=santas[i],
                        giftee=giftees[i]
                    )
                    secret_santas.append(secretsanta_pair)

                # Giftees become Santas
                shuffle(santas)
                for i in range(len(santas)):
                    secretsanta_pair = SecretSanta.objects.create(
                        date=str(datetime.datetime.now().date()),
                        santa=giftees[i],
                        giftee=santas[i]
                    )
                    secret_santas.append(secretsanta_pair)

                # Make P&C the Santa for those not picked
                admin = User.objects.get(email="shufflebox@andela.com")
                if remainder is not None:
                    secret_santas.append(
                        SecretSanta.objects.create(
                            date=str(datetime.datetime.now().date()),
                            santa=admin,
                            giftee=remainder
                        )
                    )

                serialized_data = serialize_secretsanta(secret_santas)
                return Response(
                    serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "Bad Request With Wrong Unexpected Value of 'type' key",
                    status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(
                "Bad Request: Missing Either 'type' or 'limit' ",
                status=status.HTTP_400_BAD_REQUEST)

class SendMailView(APIView):
    """View for sending out emails"""
    def post(self, request):
        try:
            request_type = request.data.get('type')
            if request_type == "brownbag":
                # TODO: add logic for sending out brownbag emails
                pass
            elif request_type == "hangout":
                # TODO:add logic for sending out hangout emails
                pass
            elif request_type == "secretsanta":
                santas = SecretSanta.objects.all()
                mail = SendMail()
                mail.subject = "Secret Santa"
                with open('secretsanta.txt', 'r') as f:
                    message = f.readlines()
                message = ''.join(message)
                for santa in santas:
                    gifter = santa.santa
                    giftee = santa.giftee.email
                    if validate_address(gifter.email) and validate_address(giftee):
                        mail.santa_message(
                            message.format(gifter.get_full_name(), giftee),giftee,gifter.email, gifter.get_full_name()
                        )
                    else:
                        mail.subject = "Secret Santa Error"
                        mail.message = "Invalid email address {} for the santa or {} for the giftee.".format(gifter, giftee)
                        mail.notify_admin()
                return Response(
                    "Succesfully sent out secret santa emails", status=status.HTTP_200_OK
                )
            else:
                return Response(
                    "Bad Request With Wrong Unexpected Value of 'type' key",
                    status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response("Bad Request: Missing 'type'", status=status.HTTP_400_BAD_REQUEST)



def serialize_secretsanta(secretsanta_data):
    """Serialize secret santa data"""
    data = {}
    count = 1
    for secretsanta in secretsanta_data:
        serializer = SecretSantaSerializer(secretsanta)
        data.update({count: json_renderer(serializer.data)})
        count += 1
    return data


def serialize_brownbag(brownbag_data):
    """Serialize the data returned depending on type of object passed."""
    data = {}
    if type(brownbag_data) == list:
        serializer = []
        count = 1
        for brownbag in brownbag_data:
            serializer = BrownbagSerializer(brownbag)
            data.update({count: json_renderer(serializer.data)})
            count += 1
    else:
        serializer = BrownbagSerializer(brownbag_data)
        data = json_renderer(serializer.data)
    return data


def json_renderer(data):
    """Render serialized data in json format"""
    rendered_data = JSONRenderer().render(data).decode()
    return json.loads(rendered_data)


def last_friday(date):
    """Utility method to find last friday of the month using a given date."""
    year = date.year
    month = date.month
    month_start = datetime.date(year, month, 1)
    return month_start + relativedelta(
        days=calendar.monthrange(year, month)[1],
        weekday=FR(-1))


def next_friday(today):
    """Utility method to return the next friday relative to the current day."""
    # gets the next friday even when we are on Friday
    friday = today + datetime.timedelta(
        ((calendar.FRIDAY - 1) - today.weekday()) % 7 + 1)
    return friday


def check_date(date):
    """Check if the date of the next friday is not already in the database"""
    try:
        if next_friday(date) <= Brownbag.objects.latest('date').date:
            raise IntegrityError
        else:
            return True
    except Brownbag.DoesNotExist:
        return True


def check_people(people):
    """Check that the number of multiple presenters is not larger than available people"""
    users = User.objects.filter(
        brownbag__isnull=True).values_list('id', flat=True)
    if people > len(users):
        return False, len(users)
    return True, len(users)


def render_json(serializer_class):
    """
    This decorator intercepts a model instance and renders it in json format.
    """
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            serializer = serializer_class(result)
            rendered = JSONRenderer().render(serializer.data)
            return json.loads(rendered.decode())
        return wrapped
    return wrapper


@render_json(HangoutSerializer)
def create_hangout(*, group_size=HANGOUT_GROUP_LIMIT):
    """
    Create a hangout group dated last friday of the month, given a group size.
    """
    # Get all users IDs elligible for brownbag
    users = User.objects.all().values_list('id', flat=True)
    rand = Randomizer(list(users))
    random_groups = rand.create_groups(group_size)
    hangout = Hangout.objects.create(date=last_friday(datetime.datetime.now()))

    for group in random_groups:
        group_object = Group.objects.create(hangout=hangout)
        for member in group:
            if member:
                group_object.members.add(member)
    return hangout


def create_brownbag(date, people):
    """
    Create a brownbag, maintaining a unique date for it.
    """
    people = 1 if people is None else int(people)
    users_queryset = User.objects.filter(
        brownbag__isnull=True).values_list('id', flat=True)

    if people > 1:
        brownbags = []
        for person in range(people):
            brownbags.append(create_brownbag(date, None))
        return brownbags
    else:
        rand = Randomizer(list(users_queryset))
        try:
            next_presenter_id = rand.get_random()
        except IndexError as e:
            # Cannot choose from an empty sequence since list is empty.
            raise
        else:
            user = User.objects.get(pk=next_presenter_id)
            brownbag = Brownbag.objects.create(
                date=next_friday(date),
                status=Brownbag.NEXT_IN_LINE,
                user=user)
            return brownbag


class HangoutView(generics.ListAPIView):
    """A view for creating new hangouts and listing them."""
    queryset = Hangout.objects.all()
    serializer_class = HangoutSerializer


class HangoutDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a hangout instance."""
    queryset = Hangout.objects.all()
    serializer_class = HangoutSerializer


class BrownbagView(generics.ListAPIView):
    """A view for listing brownbags."""
    queryset = Brownbag.objects.all()
    serializer_class = BrownbagSerializer


class BrownbagDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a brownbag instance."""
    queryset = Brownbag.objects.all()
    serializer_class = BrownbagSerializer


class BrownbagUserListView(generics.ListAPIView):
    """
    A view for getting a list of users who have not done brownbag
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Return a list of users who haven't done brownbag yet.
        """
        return User.objects.filter(brownbag__isnull=True)


class BrownbagNextInLineView(generics.ListAPIView):
    """This view  queries for the next in line brownbag presenter."""
    serializer_class = BrownbagSerializer

    def get_queryset(self):
        return Brownbag.objects.filter(status="next_in_line")


class SecretSantaView(generics.ListCreateAPIView):
    """A view for creating a new SecretSanta pair and listing all pairs."""
    queryset = SecretSanta.objects.all()
    serializer_class = SecretSantaSerializer


class SecretSantaDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """A view for retrieving, updating and deleting a Secret santa instance."""
    queryset = SecretSanta.objects.all()
    serializer_class = SecretSantaSerializer
