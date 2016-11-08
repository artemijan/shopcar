from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class LightCategoryDto(ShopBaseDto):
    name = serializers.CharField()

    @classmethod
    def from_category_model(cls, category):
        dto = cls()
        dto.name = category.name
        return dto


class ProductDto(ShopBaseDto):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True, allow_blank=False)
    categories = serializers.ListField(allow_null=True, allow_empty=True)

    @classmethod
    def from_product_model(cls, product):
        dto = cls()
        dto.id = product.id
        dto.name = product.name
        if getattr(product, 'categories', None) is not None:
            dto.categories = []
            for category in product.categories:
                dto.categories.append(LightCategoryDto.from_category_model(category))
        return dto
