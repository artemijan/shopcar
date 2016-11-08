from django.db import transaction, IntegrityError
from shop_core.model.category import Category
from shop_core.model.product import Product
from shop_core.common.errors import SaveEntityError

__author__ = 'artem'


def fetch_categories():
    return list(Category.objects.all())


@transaction.atomic
def create_category(name=None):
    try:
        category = Category()
        category.name = name
        category.save()
    except IntegrityError:
        raise SaveEntityError('Can not save product.')
    return category


@transaction.atomic
def set_products(category_pk=None, product_pks=None):
    try:
        category = Category.objects.get(pk=category_pk)
        products = Product.objects.filter(pk__in=product_pks)
        category.products = products
        category.save()
    except IntegrityError:
        raise SaveEntityError('Cannot set products to category')
    return category
