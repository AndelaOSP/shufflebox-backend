"""Authenticates JWT Tokens passed in from the front end."""

from rest_framework.authentication import BaseAuthentication, \
    get_authorization_header
from django.contrib.auth.models import User
from rest_framework import exceptions
from jwt.exceptions import InvalidTokenError
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
        """Decodes the token in the Authorization header.

        Extracts the token from the Authorization header in the request
        for decoding. Raises an exception if none exists.

        Arguments:
            request: The request containing the Authorization Header.

        Returns:
            The authenticated user object and the associated token.
        """

        auth = get_authorization_header(request).split()
        token_format = 'JWT <your token here>'
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid. The Authorization Header should look as follows:'
                '{}'.format(token_format))
        self.token = auth[1]
        try:
            payload = jwt.decode(self.token, verify=False)
            return self.authenticate_credentials(payload)
        except InvalidTokenError:
            raise exceptions.AuthenticationFailed(
                'Invalid token. Please provide a valid token:')

    def authenticate_credentials(self, payload):
        """Checks for the User object associated with the user_info payload.

        Get a user whose username matches the one in the payload or create a
        new User if none exists.

        Arguments:
            token: The token to decode

        Returns:
            A tuple with the associated User object and the token."""

        user = None
        if payload:
            user_info = payload['UserInfo']
            email = user_info['email']
            username, company = email.split('@')[0], email.split('@')[1]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, email=email)
        return (user, self.token)
