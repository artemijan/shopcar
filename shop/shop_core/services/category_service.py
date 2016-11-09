from django.db import transaction, IntegrityError
from shop_core.model.category import Category
from shop_core.model.product import Product
from shop_core.common.errors import SaveEntityError, NotFoundError

__author__ = 'artem'


def get_by_id(id=None):
    try:
        return Category.objects.get(pk=id)
    except Category.DoesNotExist:
        raise NotFoundError('Cannot find category')


def remove_by_id(id=None):
    try:
        category = get_by_id(id=id)
        category.delete()
        return category
    except IntegrityError:
        raise SaveEntityError('Cannot delete category')


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
def update_category(category_pk=None, category_name=None, product_pks=None):
    try:
        category = Category.objects.get(pk=category_pk)
        if category_name is not None:
            category.name = category_name
        if product_pks is not None:
            products = Product.objects.filter(pk__in=product_pks)
            category.products = products
        category.save()
    except IntegrityError:
        raise SaveEntityError('Cannot set products to category')
    return category
