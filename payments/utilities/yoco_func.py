import hashlib
import base64
import hmac, logging
from django.conf import settings

logger = logging.getLogger("payments")
email_logger = logging.getLogger("emails")
key = settings.YOCO_API_KEY

headers= { "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

def generate_expected_signature(signed_content, secret):
    secret_bytes = base64.b64decode(secret.split('_')[1])
    hmac_signature = hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
    expected_signature = base64.b64encode(hmac_signature).decode()

    return expected_signature

def decimal_to_str(dec_value):
    return f"{dec_value}".replace(".", "")
