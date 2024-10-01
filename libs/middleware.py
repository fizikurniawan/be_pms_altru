import threading
from django.utils.translation import gettext_lazy as _
from libs.auth import decode_auth_token
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class JWTAuthentication(TokenAuthentication):
    """
    JWT token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....
    """

    keyword = "Bearer"

    def authenticate_credentials(self, key):
        from user.models import AuthToken

        _data, error = decode_auth_token(key)
        if error:
            raise exceptions.AuthenticationFailed(_(error))

        auth_token = AuthToken.objects.filter(token=key).last()
        if not auth_token:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        return auth_token.user, auth_token
