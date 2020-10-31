from django.http import HttpResponse
from requests import Response
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.renderers import JSONRenderer

from accounts.models import User
from accounts.utils import normalize_phone

renderer_classes = [JSONRenderer]


class UserMeSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('activation_code', 'password')

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if len(phone) != 12:
            raise serializers.ValidationError(_('The value is not correct phone number.'))
        return phone

    def get_token(self, obj):
        return obj.get_token().key


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'activation_code', 'password', )

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if len(phone) != 12:
            raise serializers.ValidationError(_('The value is not correct phone number.'))
        return phone

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.send_sms_activation_code(instance.create_activation_code())
        instance.save(update_fields=['activation_code'])
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=False)
    old_password = serializers.CharField(min_length=6, write_only=True, required=False)
    name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('name', 'password', 'old_password')

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(_('Provided password is wrong'))

    def update(self, instance, validated_data):
        if validated_data.get('name'):
            instance.name = validated_data.get('name')
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'name')

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if len(phone) != 12:
            raise serializers.ValidationError(_('The value is not correct phone number.'))
        return phone

    def create(self, validated_data):
        instance = User.create(validated_data['phone'], validated_data['name'], validated_data['password'], )
        instance.save(update_fields=['activation_code'])
        return instance
