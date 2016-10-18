from django.db import transaction, IntegrityError
from shop_core.model.product import Product
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
