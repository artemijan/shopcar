from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from shop_core.model.profile import Profile
from django.contrib.auth.models import UserManager

__author__ = 'artem'


class AuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        # This method is used by django auth backend to fetch user by username.
        # Overriding this method to get account by username stored in related Profile entity
        #  to allow authorization using email as well
        if '@' in username:
            return self.get(primary_email=username)
        else:
            return self.get(primary_email__profile__username=username)


class AddressableModel(models.Model):
    class Meta:
        abstract = True

    STREET_MAX_LENGTH = 100
    CITY_MAX_LENGTH = 50
    STATE_MAX_LENGTH = 50
    ZIP_MAX_LENGTH = 15
    address_street = models.CharField(max_length=STREET_MAX_LENGTH, null=True, blank=True)
    address_city = models.CharField(max_length=CITY_MAX_LENGTH, null=True, blank=True)
    address_state = models.CharField(max_length=STATE_MAX_LENGTH, null=True, blank=True)
    address_zip = models.CharField(max_length=ZIP_MAX_LENGTH, null=True, blank=True)


class ProfileEmails(models.Model):
    EMAIL_MAX_LENGTH = 70

    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, primary_key=True, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='emails')

    def __str__(self):
        return self.email


class Account(AbstractBaseUser):
    # hack for 'username' field
    USERNAME_FIELD = 'id'
    primary_email = models.OneToOneField(ProfileEmails, on_delete=models.CASCADE)
    objects = CustomUserManager()

    def __str__(self):
        return "Account: {}".format(self.primary_email.profile.username)
