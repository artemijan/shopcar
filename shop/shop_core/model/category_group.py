from django.db import models

__author__ = 'artem'


class CategoryGroup(models.Model):
    NAME_MAX_LENGTH = 70
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, null=False)

