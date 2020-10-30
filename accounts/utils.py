from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from django.utils.translation import gettext as _
import re

from sms_sender import send_sms


def authenticate_user(phone, password):
    User = get_user_model()

    if not User.objects.filter(phone=phone).exists():
        raise exceptions.NotFound(_('Account not found.'))
    if not User.objects.get(phone=phone).check_password(password):
        raise exceptions.AuthenticationFailed()
    user = authenticate(phone=phone, password=password)
    if not user or not user.is_active:
        raise exceptions.PermissionDenied(_('003'))

    token = user.get_token()

    user.save(update_fields=['last_login'])

    return user, token.key


def send_sms_account_verification(phone, code):
    message = f'Код активации: {code}'
    try:
        send_sms(phone, message)
    except:
        pass


def normalize_phone(phone):
    phone = re.sub('[^0-9]', '', phone)
    if phone.startswith('0'):
        phone = phone[1:]

    if not phone.startswith('996') and len(phone) == 9:
        phone = f'996{phone}'

    return phone


def send_sms_account_info(phone, password, parsed_from=None, link_code=None):
    message = "Dlya bystroi prodaji my takje dobavili vashe ob'yavlenie na sait Riom.kg\n"\
                f"Login {phone}\n"\
                f"Parol: {password}\n" \
                f"https://riom.kg/new/{link_code}/ vvedite novyi parol"

    try:
        send_sms(phone, message)
    except:
        pass


def send_express_create_sms(ad_id, phone, link_code, password=None):
    if password is not None:
        message = "Vashe ob'yablenie dobavleno na sait Riom.kg\n"\
                  f"Login: {phone}\n"\
                  f"Parol: {password}\n"\
                  f"Dopolnite ego po ssylke\n"\
                  f"https://riom.kg/create_express/{ad_id}/{link_code}/"
    else:
        message = "Vashe ob'yablenie dobavleno na sait Riom.kg\n" \
                  f"Dopolnite ego po ssylke\n" \
                  f"https://riom.kg/create_express/{ad_id}/{link_code}/"
    try:
        send_sms(phone, message)
    except:
        pass
