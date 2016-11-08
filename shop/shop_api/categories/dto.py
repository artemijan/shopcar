from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class LightProductDto(ShopBaseDto):
    name = serializers.CharField()

    @classmethod
    def from_product_model(cls, product):
        dto = cls()
        dto.name = product.name
        return dto


class CategoryDto(ShopBaseDto):

    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True, allow_blank=False)
    products = serializers.ListField(allow_null=True, allow_empty=True)

    @classmethod
    def from_category_model(cls, category):
        dto = cls()
        dto.id = category.id
        dto.name = category.name
        if getattr(category, 'products', None) is not None:
            dto.categories = []
            for product in category.products:
                dto.categories.append(LightProductDto.from_product_model(product))
        return dto
