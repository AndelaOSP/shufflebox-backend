import csv
import requests
from api.utils import get_slack_user_object, SendMail
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Fetches users from slack and loads them to shufflebox"

    def add_arguments(self, parser):
        # parser.add_argument('file', nargs='+', type=str)
        # parser.add_argument('email', nargs='+', type=str)
        parser.add_argument(
            '--file',
            dest='file',
            nargs='+',
            type=str,
            help='CSV file(s) containing a list of emails. DO NOT USE COMMAS TO SEPARATE THE DIFFERENT FILES e.g --file file1 file2'
        )

        parser.add_argument(
            '--email',
            dest='email',
            nargs='+',
            type=str,
            help='User(s) email with no slack accounts. DO NOT USE COMMAS TO SEPARATE THE DIFFERENT EMAILS e.g --email email1 email2'
        )

        parser.add_argument(
            '--slack',
            dest='slack',
            nargs='+',
            type=str,
            help='User(s) correct email on slack accounts. DO NOT USE COMMAS TO SEPARATE THE DIFFERENT EMAILS e.g --slack email1 email2'
        )

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(email='shufflebox@andela.com'):
                admin = User.objects.create(
                    username=settings.ADMIN_NAME,
                    first_name='Admin',
                    last_name='Shufflebox',
                    email=settings.DEFAULT_FROM_EMAIL
                )
                admin.is_superuser = True
                admin.save()
            if options['file']:
                # Fetch user objects based on their emails
                response = requests.get(
                    'https://slack.com/api/users.list?token={}'.format(
                        settings.SLACK_TOKEN))
                if response.status_code == 200 and response.json()['ok'] == True:
                    # List of users objects
                    members = response.json()['members']
                    count = 0
                    unmatched_emails = ''
                    for csv_file in options['file']:
                        with open(csv_file, 'r') as file:
                            emails = csv.reader(file)
                            for email in emails:
                                email = email[0].strip(" ")
                                if User.objects.filter(email=email):
                                    continue
                                user_obj = get_slack_user_object(email, members)
                                co_email = email.replace('com', 'co')
                                co_user_obj = get_slack_user_object(co_email, members)
                                if user_obj:
                                    user = User.objects.create_user(
                                        username=user_obj['name'],
                                        first_name=user_obj['profile'].get('first_name', ''),
                                        last_name=user_obj['profile'].get('last_name', ''),
                                        email=email
                                    )
                                    user.profile.avatar = user_obj['profile']['image_{}'.format(512)]
                                    user.profile.bio = user_obj['profile'].get('title','')
                                    user.save()
                                    count += 1
                                elif co_user_obj:
                                    user = User.objects.create_user(
                                        username=co_user_obj['name'],
                                        first_name=co_user_obj['profile'].get('first_name', ''),
                                        last_name=co_user_obj['profile'].get('last_name', ''),
                                        email=email
                                    )
                                    user.profile.avatar = co_user_obj['profile']['image_{}'.format(512)]
                                    user.profile.bio = co_user_obj['profile'].get('title', '')
                                    user.save()
                                    count += 1
                                else:
                                    unmatched_emails = unmatched_emails + email + '\r'
                    if unmatched_emails:
                        email = SendMail()
                        email.message = "The following users don't have slack accounts\r{}".format(unmatched_emails)
                        email.subject = "Users not using slack"
                        email.notify_admin()
                    if count > 0:
                        self.stdout.write(
                            self.style.SUCCESS('Successfully added {} users to shufflebox via email'.format(count)))
                    else:
                        self.stdout.write(self.style.SUCCESS('No users added to shufflebox'))
                else:
                    if response.status_code == 200:
                        self.stderr.write("Slack Error: {}. Check token".format(response.json()['error']))
                    else:
                        self.stderr.write("Response Error: {}".format(response.status_code))
            elif options['email']:
                count = 0
                for email in options['email']:
                    if User.objects.filter(email=email):
                        continue
                    user = User.objects.create_user(
                        username=email.split('@')[0],
                        first_name=email.split('.')[0],
                        last_name=email.split('.')[1].split('@')[0],
                        email=email
                    )
                    user.profile.avatar = ''
                    user.profile.bio = ''
                    user.save()
                    count += 1
                if count > 0:
                    self.stdout.write(
                        self.style.SUCCESS('Successfully added {} users to shufflebox via email'.format(count)))
                else:
                    self.stdout.write(self.style.SUCCESS('No users added to shufflebox'))
            elif options['slack']:
                # Fetch user objects based on their emails
                response = requests.get(
                    'https://slack.com/api/users.list?token={}'.format(
                        settings.SLACK_TOKEN))
                if response.status_code == 200 and response.json()['ok'] == True:
                    # List of users objects
                    members = response.json()['members']
                    count = 0
                    for email in options['slack']:
                        if User.objects.filter(email=email):
                            continue
                        user_obj = get_slack_user_object(email, members)
                        co_email = email.replace('com', 'co')
                        co_user_obj = get_slack_user_object(co_email, members)
                        if user_obj:
                            user = User.objects.create_user(
                                username=user_obj['name'],
                                first_name=user_obj['profile'].get('first_name', ''),
                                last_name=user_obj['profile'].get('last_name', ''),
                                email=email
                            )
                            user.profile.avatar = user_obj['profile']['image_{}'.format(512)]
                            user.profile.bio = user_obj['profile'].get('title', '')
                            user.save()
                            count += 1
                    if count > 0:
                        self.stdout.write(self.style.SUCCESS(
                            'Successfully added {} users to shufflebox via correct slack email'.format(count)))
                    else:
                        self.stdout.write(self.style.SUCCESS('No users added to shufflebox'))
            else:
                self.stderr.write(
                    'No options specifed. Use ./manage.py load_users_from_slack --help to check available options')
        except IntegrityError:
            pass  # user already exists
        except Exception as e:
            raise CommandError(str(e))
