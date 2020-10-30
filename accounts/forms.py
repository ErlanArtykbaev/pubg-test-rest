from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import exceptions

from .utils import normalize_phone, authenticate_user
from .validator import validate_phone, validate_code

User = get_user_model()


class APIForm(forms.Form):
    def api_method(self, *args, **kwargs):
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        if not self.is_valid():
            return {
                'status': 'error',
                'data': self.errors
            }

        return {
            'status': 'success',
            'data': self.api_method(*args, **kwargs)
        }


class SiteRegistrationForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=128, required=True)
    phone = forms.CharField(label=_('Phone'), validators=[validate_phone])
    password = forms.CharField(min_length=6, max_length=128, label=_('Password'), widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=6, max_length=128,
                                            label=_('Password confirmation'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SiteRegistrationForm, self).clean()
        phone = normalize_phone(cleaned_data['phone'])
        if User.objects.filter(phone=phone, activation_code='').exists():
            raise forms.ValidationError(_('User with this phone number already exists'))
        cleaned_data['phone'] = phone
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError(_('Wrong password confirmation'))
        return cleaned_data


class SiteLoginForm(forms.Form):
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput,
                            validators=[validate_phone])
    password = forms.CharField(min_length=6, max_length=128, label=_('Password'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SiteLoginForm, self).clean()
        phone = normalize_phone(cleaned_data['phone'])
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('User with this number does not exist'))
        cleaned_data['phone'] = phone
        return cleaned_data


class SiteActivationForm(forms.Form):
    code = forms.CharField(max_length=6, label=_('Code'), validators=[validate_code])


class SiteResendActivationForm(forms.Form):
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput,
                            validators=[validate_phone])

    def clean(self):
        cleaned_data = super(SiteResendActivationForm, self).clean()
        phone = cleaned_data['phone']
        cleaned_data['phone'] = normalize_phone(phone)
        return cleaned_data


class SiteCreateNewPassForm(forms.Form):
    code = forms.CharField(max_length=6, label=_('Code'), validators=[validate_code])
    password = forms.CharField(min_length=6, max_length=128, label=_('Password'), widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=6, max_length=128, label=_('Pass confirmation'),
                                            widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SiteCreateNewPassForm, self).clean()
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError(_('Wrong password confirmation'))
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    old_password = forms.CharField(max_length=50, required = False)
    new_password = forms.CharField(max_length=50, required = False)
    confirm_password = forms.CharField(max_length=50, required = False)

    class Meta:
        model = User
        fields = ('name',)

    def clean(self):
        user = super(UserUpdateForm, self).save(commit=False)
        cleaned_data = super(UserUpdateForm, self).clean()
        name = cleaned_data.get('name', None)
        old_password = cleaned_data.get('old_password', None)
        new_password = cleaned_data.get('new_password', None)
        confirm_password = cleaned_data.get('confirm_password', None)

        if not name.replace(" ", ""):
            raise forms.ValidationError(_("Name cannot be empty"))

        if new_password != '':
            if new_password != confirm_password:
                raise forms.ValidationError(_("The passwords do not match"))
            if not (user.check_password(old_password)):
                raise forms.ValidationError(_('Old password is incorrect'))
            if len(confirm_password) < 6:
                raise forms.ValidationError(_('Minimum 6 characters'))

        return cleaned_data

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name', None)
        confirm_password = cleaned_data.get('confirm_password', None)
        if name:
            user.name = name
        if confirm_password:
            user.set_password(confirm_password)
        user.save()
        return user


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(min_length=6, max_length=128,
                               label=_('Password'), widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=6, max_length=128,
                                            label=_('Pass confirmation'),
                                            widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError(_('Wrong password confirmation'))
        return cleaned_data


class LoginForm(APIForm):
    phone = forms.CharField(min_length=3, max_length=32, validators=[validate_phone])
    password = forms.CharField(min_length=6, max_length=128)

    def api_method(self):
        return authenticate_user(phone=self.cleaned_data['phone'], password=self.cleaned_data['password'])

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = normalize_phone(phone)
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('User with phone number {phone} does not exist').format(phone=phone))

        return phone


class LostPasswordForm(APIForm):
    phone = forms.CharField(min_length=3, max_length=32, validators=[validate_phone])

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data['phone'])
        return phone

    def api_method(self, *args, **kwargs):
        try:
            user = User.objects.get(phone=self.cleaned_data['phone'])
        except User.DoesNotExist:
            raise exceptions.NotFound(_('Account not found'))
        user.create_activation_code()
        user.is_active = False
        user.save(is_sms_activation=True)
        return user.activation_code


class CreateNewPasswordForm(APIForm):
    phone = forms.CharField(min_length=9, validators=[validate_phone])
    password = forms.CharField(min_length=6)

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data['phone'])
        return phone

    def clean(self):
        phone = self.cleaned_data['phone']
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('Account with this phone number not found'))
        return self.cleaned_data

    def api_method(self, *args, **kwargs):
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise exceptions.NotFound(_('Account not found.'))

        user.create_new_password(password)

        return authenticate_user(phone=phone, password=password)


class ActivateAccountForm(APIForm):
    code = forms.CharField()

    def clean_code(self):
        code = self.cleaned_data['code']

        if len(str(code)) != 6:
            raise forms.ValidationError(_('Format error.'))

        if not User.objects.filter(activation_code=code, is_active=False).exists():
            raise forms.ValidationError(_('Could not find user to activate'))

        return code

    def api_method(self, *args, **kwargs):
        user = User.objects.filter(activation_code=self.cleaned_data['code'], is_active=False).last()
        user.activate_with_code(self.cleaned_data['code'])
        return user


class ResendActivationForm(APIForm):
    phone = forms.CharField(min_length=9, max_length=32, validators=[validate_phone])

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data['phone'])
        if not User.objects.filter(phone=phone, is_active=False).exists():
            raise forms.ValidationError(_('Inactive account not found.'))
        return phone

    def api_method(self, *args, **kwargs):
        try:
            user = User.objects.get(phone=self.cleaned_data['phone'], is_active=False)
        except User.DoesNotExist:
            raise exceptions.NotFound(_('Could not find user to activate'))
        user.create_activation_code()
        user.save(is_sms_activation=True)
        return user.activation_code
