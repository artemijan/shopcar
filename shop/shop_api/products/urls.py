from shop_api.products.controllers import *

from django.conf.urls import url

__author__ = 'artem'

urlpatterns = [
    url(r'^list$', ListController.as_view()),
    url(r'^$', ManageController.as_view())
]