from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from accounts.utils import normalize_phone

User = get_user_model()


def validate_phone(value):
    value = normalize_phone(value)
    if len(value) != 12:
        raise ValidationError(_('Format error.'))
    return value


def validate_code(value):
    if not value.isdigit():
        raise ValidationError(_('Activation code should contain digits only'))
    if len(value) != 6:
        raise ValidationError(_('Activation code must contain 6 digits'))
    if not User.objects.filter(activation_code=value).exists():
        raise ValidationError(_('Wrong activation code'))
    return value
