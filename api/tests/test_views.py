from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class UserViewTestCase(TestCase):
    """Test case for the user related views."""

    def setUp(self):
        """Set up the test variables."""
        pass

    def test_api_can_create_user(self):
        """Tests that the API has user creation capability."""
        pass

    def test_api_can_list_all_users(self):
        """Tests that API has user listing capability."""
        pass


class BrownbagViewTestCase(TestCase):
    """Test suite for the brown bag related views."""

    def setUp(self):
        """Set up the test variables."""
        pass

    def test_view_can_get_next_presenter(self):
        """Tests that the API can get the next brown bag presenter."""
        pass


class HangoutTestCase(TestCase):
    """Test suite for the hangout related views."""

    def setUp(self):
        """Set up the test variables."""
        pass

    def test_api_can_create_hangout(self):
        """Tests that API has hangouts creation capability."""
        pass


class SecretSantaViewTestCase(TestCase):
    """Test class for secret santa related views."""

    def setUp(self):
        """Set up test variables."""
        pass

    def test_api_can_create_secretsanta(self):
        """Test that API can create a SecretSanta."""
        pass
