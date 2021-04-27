import re

from wtforms import ValidationError
from model import User

def validate_phone(form, field):
    phone = field.data
    pattern = "^[0][9][0-9]{8}$"
    if not re.search(pattern, phone):
        raise ValidationError("Wrong phone number")
    return field


def validate_birth(form, field):
    birth = field.data
    pattern = "(\d{4})-(\d{2})-(\d{2})"
    if not re.search(pattern, str(birth)):
        raise ValidationError("ex:2000-01-01")
    return field


def validate_username(form, field):
    username = User.query.filter_by(username=field.data).first()
    if username:
        raise ValidationError("Duplicate Username")
    return field


def validate_email(form, field):
    email = User.query.filter_by(email=field.data).first()
    if email:
        raise ValidationError("Duplicate Email")
    return field


def validate_loginusername(form, field):
    user = User.query.filter(User.username==field.data).first()
    if user is None:
        raise ValidationError("Can't find this Username")
    return field
