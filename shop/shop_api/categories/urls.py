from shop_api.categories.controllers import *

from django.conf.urls import url
__author__ = 'artem'

urlpatterns = [
    url(r'^list$', ListController.as_view()),
    url(r'^(?P<category_id>[0-9]+)$', ManageController.as_view())
]
