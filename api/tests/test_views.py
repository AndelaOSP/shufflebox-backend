from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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
        self.assertEquals(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_list_all_users(self):
        """Tests that API has user listing capability."""
        res = self.client.get('/api/users/', format="json")
        self.assertEquals(res.status_code, status.HTTP_200_OK)


class ShuffleViewTestCase(TestCase):
    """Test suite for the shuffling view."""
    def setUp(self):
        self.client = APIClient()
        self.hangout = {
            'type': "hangout", "limit": 6, "notify": True
        }
        self.brownbag = {
            "type": "brownbag", "limit": 1, "notify": True
        }
        self.secretsanta = {
            "type": "secretsanta", "limit": 2, "notify": True
        }

    def test_view_can_generate_hangout_groups(self):
        res = self.client.post('/api/shuffle/', self.hangout, format="json")
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_view_can_generate_next_brownbag(self):
        res = self.client.post('/api/shuffle/', self.brownbag, format="json")
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_view_can_generate_secretsanta_pairs(self):
        res = self.client.post('/api/shuffle/', self.secretsanta, format="json")
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)


class BrownbagViewTestCase(TestCase):
    """Test suite for the brown bag related views."""

    def setUp(self):
        """Set up the test variables."""
        self.client = APIClient()
        self.brownbag = {

            status: 'nextInLine',
        }

    def test_view_can_get_next_presenter(self):
        """Tests that the API can get the next brown bag presenter."""
        pass

    def test_api_can_get_list_of_those_not_presented(self):
        """Tests that the API can list users who have never done a brownbag."""
        pass


class HangoutTestCase(TestCase):
    """Test suite for the hangout related views."""

    def setUp(self):
        """Set up the test variables."""
        pass

    def test_api_can_create_hangout(self):
        """Tests that API has hangouts creation capability."""
        pass

    def test_api_can_list_all_hangouts(self):
        """Tests that API has hangout listing capability."""
        pass


class SecretSantaViewTestCase(TestCase):
    """Test class for secret santa related views."""

    def setUp(self):
        """Set up test variables."""
        pass

    def test_api_can_create_secretsanta(self):
        """Test that API can create a SecretSanta."""
        pass

    def test_api_can_list_secretsanta(self):
        """Test that API can list all SecretSanta pairs."""
        pass
