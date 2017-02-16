from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime


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
        self.client = APIClient()

        self.hangout_request = {
            'type': 'hangout', 'limit': 2,
        }
        self.brownbag_request = {
            "type": "brownbag", "limit": 1,
        }
        self.secretsanta_request = {
            "type": "secretsanta", "limit": 2,
        }

        self.hangout_data = {
            "date": str(datetime.datetime.now().date()),
            "members": [self.test_user0.id, self.test_user1.id]
        }

        self.brownbag_data = {
            "date": str(datetime.datetime.now().date()),
            "status": "next_in_line",
            "user_id": self.test_user0.id
        }

        self.secretsanta_data = {
            "date": str(datetime.datetime.now().date()),
            "santa": self.test_user0.id,
            "giftee": self.test_user1.id
        }


class ShuffleViewTestCase(InitTestCase):
    """Test suite for the shuffling view."""

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


class BrownbagViewTestCase(InitTestCase):
    """Test suite for the brown bag related views."""

    def test_view_can_get_next_presenter(self):
        """Tests that the API can get the next brown bag presenter."""
        pass

    def test_api_can_get_list_of_those_not_presented(self):
        """Tests that the API can list users who have never done a brownbag."""
        pass


class HangoutTestCase(InitTestCase):
    """Test suite for the hangout related views."""

    def test_api_can_create_hangout(self):
        """Tests that API has hangouts creation capability."""
        res = self.client.post(
            '/api/hangout/', self.hangout_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    def test_api_can_list_all_hangouts(self):
        """Tests that API has hangout listing capability."""
        res = self.client.get('/api/hangout/', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class SecretSantaViewTestCase(InitTestCase):
    """Test class for secret santa related views."""

    def test_api_can_create_secretsanta(self):
        """Test that API can create a SecretSanta."""
        res = self.client.post(
            '/api/santa/', self.secretsanta_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    def test_api_can_list_secretsanta(self):
        """Test that API can list all SecretSanta pairs."""
        res = self.client.get('/api/hangout/', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
