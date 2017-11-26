import requests
from decouple import config
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetch users from user microservice \
            and load them to the db"

    def handle(self, *args, **options):
        headers = {
            "Authorization": config("USER_API_TOKEN", default=''),
            "Content-Type": "Application/json"
        }
        response = requests.get(
            "{}?{}".format(config("USER_SERVICE_URL", default=''),
                           config("FILTER_PARAMS", default='')),
            headers=headers)
        if response.status_code == 200:
            # Loop though the users and add them to the db
            persons = response.json()["values"]
            count = 0
            for person in persons:
                try:
                    user = User.objects.create_user(
                        username='',
                        first_name=person["first_name"],
                        last_name=person["last_name"],
                        email=person["email"]
                    )
                    user.profile.avatar = person["picture"]
                    user.profile.bio = person["bio"]
                    user.save()
                    count += 1
                except Exception:
                    # User already exists
                    pass
            self.stdout.write("Added {} users to shufflebox".format(count))
        else:
            self.stdout.write("Error: {}".format(response.status_code))
            return None
