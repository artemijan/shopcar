from django.db import transaction, IntegrityError
from shop_core.model.category_group import CategoryGroup
from shop_core.common.errors import SaveEntityError, NotFoundError

__author__ = 'artem'


def get_by_id(id=None):
    try:
        return CategoryGroup.objects.get(pk=id)
    except CategoryGroup.DoesNotExist:
        raise NotFoundError('Cannot find category group')


def remove_by_id(id=None):
    try:
        category_group = get_by_id(id=id)
        category_group.delete()
        return category_group
    except IntegrityError:
        raise SaveEntityError('Cannot delete category group')


def fetch_category_groups():
    return list(CategoryGroup.objects.all())


@transaction.atomic
def create_category_group(name=None):
    try:
        category_group = CategoryGroup()
        category_group.name = name
        category_group.save()
    except IntegrityError:
        raise SaveEntityError('Can not save category group.')
    return category_group


@transaction.atomic
def update_category_group(category_group_pk=None, category_group_name=None):
    try:
        category_group = CategoryGroup.objects.get(pk=category_group_pk)
        if category_group_name is not None:
            category_group.name = category_group_name
        category_group.save()
    except IntegrityError:
        raise SaveEntityError('Cannot update category group')
    except CategoryGroup.DoesNotExist:
        raise SaveEntityError('Cannot find category group to update')
    return category_group
