from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from datetime import datetime, timedelta
import six
import jwt


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )
    
def generate_activation_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'username': user.username,
        'exp': datetime.now() + timedelta(hours=24)  # Token valid for 24 hours
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_activation_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")



account_activation_token = AccountActivationTokenGenerator()