from datetime import datetime
import uuid, re, logging
from django.db import models
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_sa_id_number(id_number):
    error_messages = error_messages = {"success": True, "message": "ID number is valid"}

    if not re.match(r'^\d{13}$', id_number):
        error_messages = {"success": False, "message": "ID number should contain 13 numbers"}

    year = int(id_number[0:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])

    try:
        dob = datetime(year + 1900, month, day)

    except ValueError:
        error_messages = {"success": False, "message": "Your ID number is invalid"}

    if not (int(id_number[10]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
        error_messages = {"success": False, "message": "Your ID number is invalid"}

    check_sum = 0
    for i in range(13):
        digit = int(id_number[i])
        if i % 2 == 0:
            check_sum += digit
        else:
            check_sum += sum(divmod(digit * 2, 10))
    valid_check = check_sum % 10 == 0
    if not valid_check:
        error_messages = {"success": False, "message": "Your ID number is invalid"}

    return error_messages

def validate_sa_passport_number(passport_number):
    if not re.match(r'^[A-Z]{2}\d{8}$', passport_number):
        return False

    year = int(passport_number[2:4])

    current_year = datetime.now().year % 100
    if not (20 <= year <= current_year):
        return False

    return True

def verify_rsa_phone():
    PHONE_REGEX = RegexValidator(r'^(\+27|0)[1-8][0-9]{8}$', 'RSA phone number is required')
    return PHONE_REGEX

def validate_fcbk_link(value):
    url_validator = URLValidator()
    facebook_regex = r'^https?://(www\.)?facebook\.com/.*$'
    if re.match(facebook_regex, value) == None:
        raise ValidationError('Invalid Facebook profile link')
    
def validate_twitter_link(value):
    url_validator = URLValidator()
    twitter_regrex = r'^https?://(www\.)?twitter\.com/.*$'
    if re.match(twitter_regrex, value) == None:
        raise ValidationError('Invalid Twitter profile link')

def validate_insta_link(value):
    url_validator = URLValidator()
    instagram_regex = r'^https?://(www\.)?instagram\.com/.*$'
    if re.match(instagram_regex, value) == None:
        raise ValidationError('Invalid Instagram profile link')
    
def validate_in_link(value):
    url_validator = URLValidator()
    linkedin_regex = r'^https?://(www\.)?linkedin\.com/.*$'
    if re.match(linkedin_regex, value) == None:
        raise ValidationError('Invalid LinkedIn profile link')
