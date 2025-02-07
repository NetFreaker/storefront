from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationFromCookie(BaseAuthentication):
    """Custom authentication class to get JWT from HttpOnly cookies."""

    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')  # Get token from cookies

        if not access_token:
            return None  # No authentication if token not found

        try:
            # Decode and verify token
            decoded_token = AccessToken(access_token)
            user = User.objects.get(id=decoded_token['user_id'])
            return (user, None)  # DRF expects a tuple (user, auth)
        except Exception:
            raise AuthenticationFailed('Invalid or expired token')
