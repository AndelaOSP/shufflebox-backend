import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
import urllib.request as urllib

from django.conf import settings
from django.core import validators
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_framework import exceptions


class DefaultMail(object):
    """
    Common email class settings
    """

    def __init__(self):
        self.message_list = []
        self.subject = 'No subject'
        self.body = 'No body'
        self.from_email = "{} <{}>".format(settings.ADMIN_NAME.upper(), settings.DEFAULT_FROM_EMAIL)
        self.recipients = []
        self.data = {}
        self.global_data = {}


class MailGun(DefaultMail):
    """
    Class to handle mail gun emails
    """

    def send_single_mail(self, recipients):
        """Sends out a single email"""
        self.recipients.append(recipients)
        send_mail(self.subject, self.body, self.from_email, self.recipients)

    def send_batch_html_mail(self, html, request_type):
        """Send out batch html messages"""
        message = EmailMultiAlternatives(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.recipients,
            reply_to=[self.from_email]
        )
        message.attach_alternative(html, "text/html")
        message.tags = ["shufflebox", request_type]
        message.merge_data = self.data
        message.merge_global_data = self.global_data
        message.send()

    def notify_admin(self):
        """Sends out an email to the defined admins"""
        try:
            with open('templates/error.html', 'r') as f:
                html = f.readlines()
            html = ''.join(html)
            if settings.ADMINS:
                for admin in settings.ADMINS:
                    admin_name = admin[0]
                    recipient = admin[1]
                    mail_msg = EmailMultiAlternatives(
                        from_email=self.from_email,
                        subject=self.subject,
                        to=[recipient],
                        body=self.body,
                        reply_to=[self.from_email]
                    )
                    mail_msg.attach_alternative(html.format(admin_name, self.body), "text/html")
                    mail_msg.tags = ["shufflebox", "error", "bug"]
                    mail_msg.send()
            else:
                raise exceptions.ValidationError(
                    "Admin list should not be empty")
        except urllib.HTTPError as e:
            return str(e)


class SendGrid(DefaultMail):
    """
    Class to handle sending of emails from sendgrid
    """

    def __init__(self):
        self.send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = Email(email=settings.DEFAULT_FROM_EMAIL, name='SHUFFLEBOX')
        super(SendMail, self).__init__()

    def notify_admin(self):
        """Sends out an email to the defined admins"""
        try:
            if settings.ADMINS:
                for admin in settings.ADMINS:
                    admin_name = admin[0]
                    recipient = Email(admin[1])
                    content = Content('text/html', self.message)
                    mail_msg = Mail(from_email=self.from_email, subject=self.subject, to_email=recipient,
                                    content=content)
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-admin-', value=admin_name))
                    mail_msg.personalizations[0].add_substitution(Substitution(key='-body-', value=self.message))
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
