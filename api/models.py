from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    """Class definition for the User Profile model.

    Extends default django User model that stores username, email, pword etc
    """

    # Helper callable model variables
    NEXT_IN_LINE = "next_in_line"
    DONE = "done"
    NOT_DONE = "not_done"

    brownbag_choices = (
        (NEXT_IN_LINE, "Next In Line"),
        (DONE, "Done"),
        (NOT_DONE, "Not Done")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(default="", max_length=500, blank=True)
    brownbag = models.CharField(
        max_length=12, choices=brownbag_choices, default=NOT_DONE)

    def __unicode__(self):
        return u'User Profile for: {}'.format(self.user.username)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "{}".format(self.user.username)


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

    # Helper callable model variables
    NEXT_IN_LINE = "next_in_line"
    DONE = "done"
    NOT_DONE = "not_done"

    brownbag_choices = (
        (NEXT_IN_LINE, "Next In Line"),
        (DONE, "Done"),
        (NOT_DONE, "Not Done")
    )

    date = models.DateField(blank=True)
    status = models.CharField(
        max_length=12, choices=brownbag_choices, default=NOT_DONE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "{} Status: {}".format(self.user, self.status)


class Hangout(models.Model):
    """Class definition for the Hangout model."""
    date = models.DateField()
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        """Return a string representation of the model instance."""
        return "Hangout: {}, Members: {}".format(self.pk, self.members.all())

    def __unicode__(self):
        return self.members


class SecretSanta(models.Model):
    """Class definition for the Secret santa model."""
    date = models.DateField()
    santa = models.ForeignKey(
        User, related_name="santa", on_delete=models.CASCADE)
    giftee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "Santa: {}, Giftee: {}".format(self.santa, self.giftee)
