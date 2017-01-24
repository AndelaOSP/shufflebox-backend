from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    """Class definition for the User Profile model.

    Extends default django User model that stores username, email, pword etc
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(default="", max_length=500, blank=True)

    def __unicode__(self):
        return u'User Profile for: {}'.format(self.user.username)


# Decorator to pass in a post_save signal
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to create a user profile when a User instance is created."""

    if created:
        Profile.objects.create(user=instance)


# Decorator to pass in a post_save signal
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to update a user profile when a User instance is updated."""
    instance.profile.save()


class BrownBag(models.Model):
    """Class definition for the BrownBag model."""
    date = models.DateField(blank=True)
    status = models.CharField(max_length=20, default="not done")
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
