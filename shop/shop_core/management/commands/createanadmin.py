import sys

from django.core.management.base import BaseCommand, CommandError
from shop_core.model.auth import Account, ProfileEmails
from shop_core.services import account_service
from shop_core.model.profile import Profile
from django.core import exceptions
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def get_input_data(self, field, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.
        """
        raw_value = input(message)
        if default and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None

        return val

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        first_name = self.get_input_data(Profile._meta.get_field('first_name'), 'Please enter first name: ')
        last_name = self.get_input_data(Profile._meta.get_field('last_name'), 'Please enter last name: ')
        username = self.get_input_data(Profile._meta.get_field('username'), 'Please enter username: ')
        email = self.get_input_data(ProfileEmails._meta.get_field('email'), 'Please enter an email: ')
        password = self.get_input_data(Account._meta.get_field('password'), 'Please enter password: ')
        password_again = None
        while password_again != password:
            password_again = self.get_input_data(Account._meta.get_field('password'), 'Please enter password (again): ')
        account_service.create_account(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        self.stdout.write('Successfully created account!')
