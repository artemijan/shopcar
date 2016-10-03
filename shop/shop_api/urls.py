from django.conf.urls import url, include
__author__ = 'artem'

urlpatterns = [
    url(r'^auth/', include('shop_api.auth.urls'))
]
