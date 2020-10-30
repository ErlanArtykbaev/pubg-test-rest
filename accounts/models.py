from datetime import timezone

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from accounts.manager import UserManager
from accounts.utils import send_sms_account_verification
from sms_sender import *


class User(AbstractBaseUser):
    phone = models.CharField(max_length=30, unique=True, verbose_name=_('Phone'))
    name = models.CharField(max_length=50, blank=True, verbose_name=_('Name'))
    contact_number = models.CharField(max_length=100, blank=True,
                                      verbose_name=_('Contact Number'))
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                  verbose_name=_('Name'))

    activation_code = models.CharField(max_length=6, blank=True,
                                       verbose_name=_('Activation Code'))

    date_joined = models.DateField(auto_now_add=True, verbose_name=_('Date joined'))
    device_id = models.CharField(max_length=255, blank=True)
    link_code = models.CharField(max_length=8, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.name} {self.phone}'

    @classmethod
    def create(cls, phone, password, is_sms_activated=True, **kwargs):
        user = cls(phone=phone, **kwargs)
        user.set_password(password)
        user.activation_code = get_random_string(6, '0123456789')
        user.save(is_sms_activation=is_sms_activated)
        return user

    def create_new_password(self, password):
        self.set_password(password)
        self.activation_code = ''
        self.save(update_fields=['activation_code', 'password'])
        return True

    def create_activation_code(self):
        code = get_random_string(6, '0123456789')
        self.activation_code = code
        self.save(update_fields=['activation_code'])
        return code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception(_('code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])
        return True

    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)

        return token

    def send_sms_activation_code(self, code):
        send_sms_account_verification(self.phone, code)
        return True

    def save_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
# Create your models here.
