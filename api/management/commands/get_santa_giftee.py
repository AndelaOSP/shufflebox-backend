from api.models import SecretSanta
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'gets the giftee or santa for the given email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--santa',
            dest='santa',
            nargs='+',
            type=str,
            help='Email(s) to get who is the santa. DO NOT USE COMMAS TO SEPARATE THE DIFFERENT FILES e.g --santa email1 email2'
        )
        parser.add_argument(
            '--giftee',
            dest='giftee',
            nargs='+',
            type=str,
            help='Email(s) to get who is the giftee. DO NOT USE COMMAS TO SEPARATE THE DIFFERENT FILES e.g --giftee email1 email2'
        )

    def handle(self, *args, **options):
        try:
            secretsanta = SecretSanta.objects.all()
            result = []
            if options['santa'] and secretsanta:
                for email in options['santa']:
                    try:
                        santa_mail =[santa.get_santa_email() for santa in secretsanta if santa.get_giftee_email() == email][0]
                        result.append('The Secret Santa for {} is {}'.format(email, santa_mail))
                    except IndexError:
                        result.append('The user {} has no Secret Santa'.format(email))
                res = [self.stdout.write(self.style.SUCCESS(res)) for res in result][0]
            elif options['giftee'] and secretsanta:
                for email in options['giftee']:
                    try:
                        giftee_mail =[giftee.get_giftee_email() for giftee in secretsanta if giftee.get_santa_email() == email][0]
                        result.append('The Giftee for {} is {}'.format(email, giftee_mail))
                    except IndexError:
                        result.append('The user {} has no giftee'.format(email))
                res = [self.stdout.write(self.style.SUCCESS(res)) for res in result][0]
            else:
                self.stderr.write(
                    'No options specifed. Use ./manage.py get_santa_gifee --help to check available options')
        except CommandError as e:
            raise CommandError(str(e))
