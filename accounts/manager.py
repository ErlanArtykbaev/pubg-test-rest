from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, phone, name, player_id, password=None):
        if not phone:
            raise ValueError(_('Please provide phone number'))

        user = self.model(phone=phone, name=name, player_id=player_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password, player_id):
        if not phone:
            raise ValueError(_('Please provide phone number'))
        user = self.model(phone=phone, name=name, player_id=player_id, is_staff=True, is_active=True)
        user.set_password(password)
        user.save(using=self._db)
        return user
