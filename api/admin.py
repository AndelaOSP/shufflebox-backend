from django.contrib import admin
from .models import Profile, Brownbag, SecretSanta, Hangout

# Register your models here.
admin.site.register(Profile)
admin.site.register(Brownbag)
admin.site.register(Hangout)
admin.site.register(SecretSanta)
