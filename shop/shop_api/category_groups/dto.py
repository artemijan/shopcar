from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class CategoryGroupDto(ShopBaseDto):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=False, allow_blank=False)

    @classmethod
    def from_category_group_model(cls, category):
        dto = cls()
        dto.id = category.id
        dto.name = category.name
        return dto
