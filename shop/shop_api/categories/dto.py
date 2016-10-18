from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class CategoryDto(ShopBaseDto):
    name = serializers.CharField()

    @classmethod
    def from_category_model(cls, category):
        dto = cls()
        dto.name = category.name
        return dto
