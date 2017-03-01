from django.test import TestCase
from api.models import Profile, BrownBag, Hangout, SecretSanta
from django.contrib.auth.models import User
from django.db import IntegrityError
from datetime import datetime


class ModelTestCase(TestCase):
    """This class defines a test suite for the core models."""

    def setUp(self):
        """Set up method to define user and other test variables."""
        self.username = "ABC"
        self.email = "abc@example.com"
        self.old_user_count = User.objects.count()
        self.user = User.objects.create(
            username=self.username, email=self.email)

        self.date = datetime.now().date()

        self.brownbag = BrownBag(date=self.date,)
        self.hangout = Hangout(date=self.date,)
        self.secretsanta = SecretSanta(date=self.date)

    def test_user_creation(self):
        """Test a user can be created."""
        self.new_user_count = User.objects.count()
        self.assertNotEqual(self.old_user_count, self.new_user_count)
        self.assertIsInstance(self.user, User)

    def test_user_profile_creation_already(self):
        """Test one to one relationship between profile and user created.
        Confirms that duplicate key values will not be written on the DB"""
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.user)

    def test_hangout_creation(self):
        """Test a hangout group can be created"""
        self.count = Hangout.objects.count()
        self.hangout = Hangout.objects.create(date=self.date)
        self.new_count = Hangout.objects.count()
        self.assertNotEqual(self.count, self.new_count)

    def test_adding_members_to_a_hangout(self):
        """Test that a hangout can add members."""
        self.count = Hangout.objects.count()
        self.hangout = Hangout.objects.create(date=self.date)
        self.count = self.hangout.members.count()
        self.hangout.members.add(self.user)
        self.new_count = self.hangout.members.count()
        self.assertNotEqual(self.count, self.new_count)

    def test_brownbag_creation(self):
        """Test a BrownBag can be created."""
        self.count = BrownBag.objects.count()
        self.brownbag = BrownBag.objects.create(
            date=self.date, status="not done", user=self.user)
        self.new_count = BrownBag.objects.count()
        self.assertNotEqual(self.count, self.new_count)

    def test_secret_santa_creation(self):
        """Test a SecretSanta can be created."""
        self.count = SecretSanta.objects.count()
        giftee = User.objects.create(username="giftee", email="g@gmail.com")
        santa = SecretSanta.objects.create(
            date=self.date,
            santa=self.user,
            giftee=giftee
        )
        self.new_count = SecretSanta.objects.count()
        self.assertNotEqual(self.count, self.new_count)

    def test_models_return_human_readable_representation(self):
        """Test the models instances return a string."""
        self.assertEqual(str(self.user), self.username)
