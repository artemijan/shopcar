from dto import ShopBaseDto
from rest_framework import serializers

__author__ = 'artem'


class LightProductDto(ShopBaseDto):
    name = serializers.CharField()

    @classmethod
    def from_product_model(cls, product):
        dto = cls()
        dto.name = product.name
        return dto.to_dict()


class LightCategoryGroupDto(ShopBaseDto):
    name = serializers.CharField()
    id = serializers.IntegerField()

    @classmethod
    def from_category_group_model(cls, category_group):
        dto = cls()
        dto.name = category_group.name
        dto.id = category_group.id
        return dto.to_dict()


class CategoryDto(ShopBaseDto):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True, allow_blank=False)
    products = serializers.ListField(allow_null=True, allow_empty=True)
    group = serializers.IntegerField(allow_null=True)

    @classmethod
    def from_category_model(cls, category):
        dto = cls()
        dto.id = category.id
        dto.name = category.name
        if getattr(category, 'products', None) is not None:
            dto.products = []
            for product in category.products:
                dto.products.append(LightProductDto.from_product_model(product))
        if getattr(category, 'category_group', None) is not None:
            dto.group = LightCategoryGroupDto.from_category_group_model(category.category_group)
        return dto.to_dict()
