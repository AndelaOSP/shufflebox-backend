from django.conf import settings
from django.core.mail import send_mail, get_connection, mail_admins, EmailMessage
from django.core import validators
from smtplib import SMTPException
from rest_framework import exceptions


class Mail(object):
    """
    Class to handle sending of emails
    """
    message_list = []
    subject = 'No subject'
    message = 'No message'

    def single_mail(self, recipient=None):
        """Sends out a single email"""
        try:
            if validate_address(recipient):
                send_mail(
                    subject=self.subject, message=self.message, from_email= settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],fail_silently=False
                )
            else:
                notify_admin('Shuffle Box Error','Invalid recipient {}'.format(recipient))
                raise exceptions.ValidationError(
                    "Email message and recipient should be included. Recipient should also be a valid email address.")
        except SMTPException as e:
            return str(e)

    def mass_mail(self):
        try:
            if self.message_list:
                connection = get_connection()
                connection.send_messages(self.message_list)
            else:
                raise exceptions.ValidationError(
                    "Message list should not be empty")
        except SMTPException as e:
            return str(e)

    def create_message(self, message='No message', recipients=None):
        try:
            if recipients and isinstance(recipients, list):
                mail_msg = EmailMessage(self.subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
                mail_msg.content_subtype = 'HTML'
                self.message_list.append(mail_msg)
            else:
                raise exceptions.ValidationError(
                    "Recipients list should not be empty")
        except SMTPException as e:
            return str(e)




def validate_address(address):
    try:
        validators.validate_email(address)
        return True
    except validators.ValidationError:
        return False


def notify_admin(subject, message):
    try:
        mail_admins(subject=subject, message=message, fail_silently=False)
    except SMTPException as e:
        return str(e)
