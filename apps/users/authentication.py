import json
import jwt
import requests as http_requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


def get_clerk_public_keys():
    response = http_requests.get(settings.CLERK_JWKS_URL)
    response.raise_for_status()
    return response.json()["keys"]


def verify_clerk_token(token):
    try:
        keys = get_clerk_public_keys()
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        matching_key = next((k for k in keys if k["kid"] == kid), None)
        if not matching_key:
            raise AuthenticationFailed("No matching key found")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(matching_key))

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationFailed(f"Invalid token: {str(e)}")


class ClerkJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        payload = verify_clerk_token(token)

        clerk_id = payload.get("sub")
        if not clerk_id:
            raise AuthenticationFailed("Invalid token payload")

        try:
            user = User.objects.get(clerk_id=clerk_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found. Please complete registration.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled")

        return (user, token)