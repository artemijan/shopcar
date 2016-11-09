from shop_api.categories.dto import CategoryDto
from shop_core.common.controllers import ShopApiView, ShopApiResponse
import shop_core.services.category_service as category_service
from shop_core.common.errors import SaveEntityError, NotFoundError

__author__ = 'artem'


class ManageController(ShopApiView):
    def post(self, request):
        dto = CategoryDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            category = category_service.create_category(name=dto.name)
            return ShopApiResponse.success(CategoryDto.from_category_model(category))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))

    def get(self, request, category_id=None):
        try:
            product = category_service.get_by_id(id=category_id)
            return ShopApiResponse.success(CategoryDto.from_product_model(product))
        except NotFoundError as e:
            return ShopApiResponse.bad_request(str(e))

    def put(self, request, category_id=None):
        dto = CategoryDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            product = category_service.update_category(category_pk=category_id, product_pks=dto.products)
            return ShopApiResponse.success(CategoryDto.from_product_model(product))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))


class ListController(ShopApiView):
    def get(self, request):
        categories = category_service.fetch_categories()
        result = []
        for product in categories:
            result.append(CategoryDto.from_category_model(product))
        return ShopApiResponse.success(result)
