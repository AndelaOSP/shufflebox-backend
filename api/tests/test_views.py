from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from unittest import skip
import datetime

from api.models import Hangout
from api.views import last_friday
import os
from api.serializers import UserSerializer


AUTH_TOKEN = 'JWT ' + os.getenv('JWT_TOKEN')


class UserViewTestCase(TestCase):
    """Test case for the user related views."""

    def setUp(self):
        """Set up the test variables."""
        self.client = APIClient()
        self.user_data = {
            'username': "test_user",
            'email': "user@example.com",
            'profile': {
                'avatar': "a_long_string.png"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_TOKEN)
        self.response = self.client.post(
            '/api/users/', self.user_data, format="json")

    def test_api_can_create_user(self):
        """Tests that the API has user creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_list_all_users(self):
        """Tests that API has user listing capability."""
        res = self.client.get('/api/users/', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class InitTestCase(TestCase):
    def setUp(self):
        self.test_user0 = User.objects.create_user(
            username="test_user0", email="user0@test.com"
        )
        self.test_user1 = User.objects.create_user(
            username="test_user1", email="user1@test.com"
        )
        self.test_user2 = User.objects.create_user(
            username="test_user2", email="user2@test.com"
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_TOKEN)
        self.hangout_request = {
            'type': 'hangout', 'limit': 1,
        }
        self.brownbag_request = {
            "type": "brownbag", 'limit': 1,
        }
        self.brownbag_multiple_request = {
            "type": "brownbag", 'limit': 3,
        }
        self.secretsanta_request = {
            "type": "secretsanta", "limit": 2,
        }

        self.hangout_data = {
            "date": str(last_friday(datetime.datetime.now().date()))
        }

        self.brownbag_data = {
            "date": str(datetime.datetime.now().date()),
            "status": "next_in_line",
            "user": UserSerializer(self.test_user0).data
        }

        self.secretsanta_data = {
            "date": str(datetime.datetime.now().date()),
            "santa": self.test_user0.id,
            "giftee": self.test_user1.id
        }


class ShuffleViewTestCase(InitTestCase):
    """Test suite for the shuffling view."""
    fixtures = ['admin.json']

    def test_view_can_generate_hangout_groups(self):
        res = self.client.post(
            '/api/shuffle/', self.hangout_request, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_view_can_generate_next_brownbag(self):
        res = self.client.post(
            '/api/shuffle/', self.brownbag_request, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_view_can_generate_secretsanta_pairs(self):
        res = self.client.post(
            '/api/shuffle/', self.secretsanta_request, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class BrownbagTestCase(InitTestCase):
    """Test suite for the brown bag related views."""

    def test_api_cannot_directly_create_next_brownbag_presenter(self):
        """Tests that the API can get the next brown bag presenter."""
        res = self.client.post(
            '/api/brownbags/', self.brownbag_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_can_update_presenter_status(self):
        """Tests that the API can update the status of a brownbag."""
        res = self.client.post(
            '/api/shuffle/', self.brownbag_request, format="json")
        # change the status from next_in_line to done
        new_data = {
            "status": "done",
            "date": res.data['date'],
            "user": res.data['user']
        }
        res = self.client.put(
            '/api/brownbags/{}/'.format(
                res.data['id']), new_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_api_can_get_a_brownbag(self):
        """Test that the API can retrieve the next presenter"""
        req = self.client.post(
            '/api/shuffle/', self.brownbag_request, format="json")
        res = self.client.get(
            '/api/brownbags/{}/'.format(req.data['id']), format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.brownbag_data['status'], res.data['status'])

    def test_api_can_create_multiple_presenters(self):
        """Test that the API can allow for multiple presenters"""
        req = self.client.post(
            '/api/shuffle/', self.brownbag_multiple_request, format="json")
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.brownbag_multiple_request['limit'], len(req.data))


class HangoutTestCase(InitTestCase):
    """Test suite for the hangout related views."""

    def test_api_cannot_create_hangout(self):
        """Tests that the API is forbidden to create hangouts directly."""
        res = self.client.post(
            '/api/hangouts/', self.hangout_data, format="json")
        self.assertEqual(
            res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, res.content)

    def test_api_can_list_all_hangouts(self):
        """Tests that API has hangout listing capability."""
        res = self.client.get('/api/hangouts/', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_get_single_hangout(self):
        """Test that the API can retrieve a single hangout."""
        req = self.client.post(
            '/api/shuffle/', self.hangout_request, format="json")
        res = self.client.get(
            '/api/hangouts/{}/'.format(req.data['id']), format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.hangout_data['date'],
            str(last_friday(datetime.datetime.now().date()))
        )


class SecretSantaViewTestCase(InitTestCase):
    """Test class for secret santa related views."""

    @skip('WIP')
    def test_api_can_create_secretsanta(self):
        """Test that API can create a SecretSanta."""
        res = self.client.post(
            '/api/santas/', self.secretsanta_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    def test_api_can_list_secretsanta(self):
        """Test that API can list all SecretSanta pairs."""
        res = self.client.get('/api/santas/', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @skip('WIP')
    def test_api_can_get_single_secretsanta_pair(self):
        """Test that the API can retrieve a single pair of secretsanta."""
        req = self.client.post(
            '/api/santas/', self.secretsanta_data, format="json")
        res = self.client.get(
            '/api/santas/{}/'.format(req.data['id']), format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.secretsanta_data['date'], res.data['date'])
