from shop_api.products.dto import ProductDto
from shop_core.common.controllers import ShopApiView, ShopApiResponse
import shop_core.services.products_service as product_service
from shop_core.common.errors import SaveEntityError

__author__ = 'artem'


class ManageController(ShopApiView):
    def post(self, request):
        dto = ProductDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            product = product_service.create_product(name=dto.name)
            return ShopApiResponse.success(ProductDto.from_product_model(product))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))

    def put(self, request, user_id=None):
        dto = ProductDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            product = product_service.update_product(product_pk=user_id, category_pks=dto.categories)
            return ShopApiResponse.success(ProductDto.from_product_model(product))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))


class ListController(ShopApiView):
    def get(self, request):
        products = product_service.fetch_products()
        result = []
        for product in products:
            result.append(ProductDto.from_product_model(product))
        return ShopApiResponse.success(result)
