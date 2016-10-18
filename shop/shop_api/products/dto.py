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
    name = serializers.CharField()

    @classmethod
    def from_product_model(cls, product):
        dto = cls()
        dto.name = product.name
        dto.categories = []
        if getattr(product, 'categories', None) is not None:
            for category in product.categories:
                dto.categories.append(LightCategoryDto.from_category_model(category))
        return dto
