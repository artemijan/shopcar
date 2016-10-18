from django.db import models

__author__ = 'artem'


class Profile(models.Model):
    USERNAME_MAX_LENGTH = 70
    NAME_MAX_LENGTH = 30

    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True, null=True)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.first_name

    def __str__(self):
        return "{} (/u/{})".format(self.first_name, self.username) if self.username is not None else self.first_name
