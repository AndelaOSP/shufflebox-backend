"""
Authenticates JWT Tokens passed in from the front end.
"""
from rest_framework.authentication import BaseAuthentication, \
    get_authorization_header
from django.contrib.auth.models import User
from rest_framework import exceptions
import jwt


class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom Token authentication.

    Clients pass in a JWT Token in the "Authorization"
    HTTP header, prepended with the string "JWT ".  For example:
        Authorization: JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
    """

    keyword = 'JWT'
    token = ''

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        token_format = 'JWT <your token here>'
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid. The Authorization Header should look as follows:'
                '{}'.format(token_format))
            return None
        token = auth[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        return self.verify_token(token)

    def verify_token(self, token):
        payload = jwt.decode(token, verify=False)
        user = None
        if payload:
            user_info = payload['UserInfo']
            email = user_info['email']
            username, company = email.split('@')[0], email.split('@')[1]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, email=email)
        return user, token

    def authenticate_header(self, request):
        return self.keyword
