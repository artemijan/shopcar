from django.db import transaction, IntegrityError
from shop_core.model.product import Product
from shop_core.model.category import Category
from shop_core.common.errors import SaveEntityError

__author__ = 'artem'


def fetch_products():
    return list(Product.objects.all())


@transaction.atomic
def create_product(name=None):
    try:
        product = Product()
        product.name = name
        product.save()
    except IntegrityError:
        raise SaveEntityError('Can not save product.')
    return product


@transaction.atomic
def update_product(product_pk=None, product_name=None, category_pks=None):
    try:
        product = Product.objects.get(pk=product_pk)
        if product_name is not None:
            product.name = product_name
        if category_pks is not None:
            categories = Category.objects.filter(pk__in=category_pks)
            product.categories = categories
        product.save()
    except IntegrityError:
        raise SaveEntityError('Cannot set categories to product')
    return product
