import django.db.transaction as transaction
from shop_core.common.errors import SaveEntityError
from shop_core.model.auth import Account, ProfileEmails
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from shop_core.model.profile import Profile
__author__ = 'artem'


def get_account_by_username(username):
    account = Account.objects.get_by_natural_key(username)
    # todo:  handle errors
    # TODO: ensure fetching of realted profile and emails
    return account


def get_account_by_email(email):
    try:
        acc = get_account_by_email(email)
        return acc
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('Could not fetch account by this email, probably account does not exist or deleted')


def get_account_by_email(email=None):
    account = Account.objects.get(primary_email=email)
    return account


@transaction.atomic
def create_account(username, email, password, first_name, last_name):
    try:
        profile = Profile()
        profile.first_name = first_name
        profile.username = username
        profile.last_name = last_name
        profile.save()

        e = ProfileEmails()
        e.email = email
        e.profile = profile
        e.save()

        acc = Account(primary_email=e)
        if password is None:
            acc.set_unusable_password()
        else:
            acc.set_password(password)
        acc.save()
        return acc
    except IntegrityError:
        raise SaveEntityError('Can not save account. Probably email already exists in the system.')

