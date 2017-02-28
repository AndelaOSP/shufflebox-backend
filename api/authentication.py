"""
Authenticates JWT Tokens passed in from the front end.
"""
from rest_framework.authentication import BaseAuthentication


class CustomTokenAuthentication(BaseAuthentication):
    """
    Token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """