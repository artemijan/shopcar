from django.conf.urls import url, include

__author__ = 'artem'

urlpatterns = [
    url(r'^auth/', include('shop_api.auth.urls')),
    url(r'^products/', include('shop_api.products.urls')),
    url(r'^categories/', include('shop_api.categories.urls')),
]
