from shop_api.auth.controllers import *

from django.conf.urls import url

__author__ = 'artem'

urlpatterns = [
    url(r'^sign_in$', SignInController.as_view()),
    url(r'^sign_up$', SignUpController.as_view()),
    url(r'^sign_out$', SignOutController.as_view())
]
