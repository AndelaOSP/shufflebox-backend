import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
import urllib.request as urllib

from django.conf import settings
from django.core import validators
from django.core.mail import send_mail
from rest_framework import exceptions


class DefaultMail(object):
    """
    Common email class settings
    """

    def __init__(self):
        self.message_list = []
        self.subject = 'No subject'
        self.message = 'No message'
        self.from_email = "{} <{}>".format(settings.ADMIN_NAME.upper(), settings.DEFAULT_FROM_EMAIL)
        self.recipients = []


class MailGun(DefaultMail):
    """
    Class to handle mail gun emails
    """

    def single_mail(self):
        send_mail(self.subject, self.message, self.from_email, self.recipients)


class SendMail(DefaultMail):
    """
    Class to handle sending of emails
    """

    def __init__(self):
        self.send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = Email(email=settings.DEFAULT_FROM_EMAIL, name='SHUFFLEBOX')
        super(SendMail, self).__init__()

    def notify_admin(self):
        """Sends out a single email"""
        try:
            if settings.ADMINS:
                for admin in settings.ADMINS:
                    admin_name = admin[0]
                    recipient = Email(admin[1])
                    content = Content('text/html', self.message)
                    mail_msg = Mail(from_email=self.from_email, subject=self.subject, to_email=recipient,
                                    content=content)
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-admin-', value=admin_name))
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-message-', value=self.message))
                    mail_msg.template_id = settings.ADMIN_TEMPLATE
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
                    Substitution(key='-date-', value=settings.END_OF_YEAR_PARTY_DATE)
                )
                mail_msg.template_id = settings.SANTA_TEMPLATE
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
