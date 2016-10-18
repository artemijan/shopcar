from dto import ShopBaseDto
from shop_core.model.profile import Profile
from rest_framework import serializers

__author__ = 'artem'


class SignInDto(ShopBaseDto):
    username = serializers.CharField()
    password = serializers.CharField()
    permanent = serializers.BooleanField(default=False)


class SignUpDto(ShopBaseDto):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserDto(ShopBaseDto):
    id = serializers.IntegerField()

    username = serializers.CharField(max_length=Profile.USERNAME_MAX_LENGTH)
    first_name = serializers.CharField(max_length=Profile.NAME_MAX_LENGTH)
    last_name = serializers.CharField(max_length=Profile.NAME_MAX_LENGTH)
    email = serializers.EmailField()

    is_admin = serializers.NullBooleanField(default=False)

    new_password = serializers.CharField(max_length=255, allow_null=True, allow_blank=False, required=False)
    password = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, required=False)

    @classmethod
    def from_account_model(cls, account):
        dto = cls()
        profile = account.primary_email.profile
        dto.id = profile.id
        dto.username = profile.username
        dto.last_name = profile.last_name
        dto.first_name = profile.first_name
        dto.email = account.primary_email.pk
        return dto
