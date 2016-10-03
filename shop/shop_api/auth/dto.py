from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class SignInDto(ShopBaseDto):
    username = serializers.CharField()
    password = serializers.CharField()
    permanent = serializers.BooleanField(default=False)
