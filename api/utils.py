import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
import urllib.request as urllib

from datetime import date
from decouple import config
from django.conf import settings
from django.core import validators
from rest_framework import exceptions


class SendMail(object):
    """
    Class to handle sending of emails
    """
    def __init__(self):
        self.message_list = []
        self.subject = 'No subject'
        self.message = 'No message'
        self.send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = Email(email=settings.DEFAULT_FROM_EMAIL, name='SHUFFLEBOX')

    def notify_admin(self):
        """Sends out a single email"""
        try:
            if settings.ADMINS:
                for admin in settings.ADMINS:
                    admin_name = admin[0]
                    recipient = Email(admin[1])
                    content = Content('text/html', self.message)
                    mail_msg = Mail(from_email=self.from_email, subject=self.subject, to_email=recipient, content=content)
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-admin-', value=admin_name))
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-message-', value=self.message))
                    mail_msg.template_id = config('ADMIN_TEMPLATE_ID', default='')
                    self.send_message(mail_msg)
            else:
                raise exceptions.ValidationError(
                    "Admin list should not be empty")
        except urllib.HTTPError as e:
            return str(e)


    def santa_message(self, message=None, giftee_email=None, recipient=None, santa_name=None):
        try:
            if recipient:
                recipient = Email(recipient)
                content = Content('text/html', message)
                mail_msg = Mail(from_email=self.from_email, subject=self.subject, to_email=recipient, content=content)
                mail_msg.personalizations[0].add_substitution(Substitution(key='-santa-', value=santa_name))
                mail_msg.personalizations[0].add_substitution(Substitution(key='-giftee-', value=giftee_email))
                mail_msg.personalizations[0].add_substitution(
                    Substitution(key='-date-', value=config('END_OF_YEAR_PARTY_DATE', default=date.today()))
                )
                mail_msg.template_id = config('SANTA_TEMPLATE_ID', default='')
                self.send_message(mail_msg)
            else:
                raise exceptions.ValidationError(
                    "Recipients list should not be empty")
        except urllib.HTTPError as e:
            return str(e)

    def send_message(self, mail):
        try:
            return self.send_grid.client.mail.send.post(request_body=mail.get())
        except Exception as e:
            self.subject = "Mail Error"
            self.message = str(e)
            self.notify_admin()



def validate_address(address):
    try:
        validators.validate_email(address)
        return True
    except validators.ValidationError:
        return False


def get_slack_user_object(email, members):
    for user in members:
        try:
            if email == user.get('profile').get('email'):
                return user
        except KeyError:
            return False