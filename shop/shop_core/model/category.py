from django.db import models
from shop_core.model.product import Product

__author__ = 'artem'


class Category(models.Model):
    NAME_MAX_LENGTH = 70

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, null=False)
    product = models.ManyToManyField(Product, related_name='products')
