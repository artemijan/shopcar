from shop_api.category_groups.dto import CategoryGroupDto
from shop_core.common.controllers import ShopApiView, ShopApiResponse
import shop_core.services.category_group_service as category_group_service
from shop_core.common.errors import SaveEntityError, NotFoundError

__author__ = 'artem'


class ManageController(ShopApiView):
    def post(self, request):
        dto = CategoryGroupDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            category_group = category_group_service.create_category_group(name=dto.name)
            return ShopApiResponse.success(CategoryGroupDto.from_category_model(category_group))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))

    def get(self, request, category_group_id=None):
        try:
            category_group = category_group_service.get_by_id(id=category_group_id)
            return ShopApiResponse.success(CategoryGroupDto.from_product_model(category_group))
        except NotFoundError as e:
            return ShopApiResponse.bad_request(str(e))

    def delete(self, request, category_group_id):
        try:
            category_group = category_group_service.remove_by_id(id=category_group_id)
            return CategoryGroupDto.from_category_model(category_group)
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))

    def put(self, request, category_group_id=None):
        dto = CategoryGroupDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            category = category_group_service.update_category_group(category_group_pk=category_group_id,
                                                                    category_group_name=dto.name)
            return ShopApiResponse.success(CategoryGroupDto.from_product_model(category))
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))


class ListController(ShopApiView):
    def get(self, request):
        category_groups = category_group_service.fetch_category_groups()
        result = []
        for product in category_groups:
            result.append(CategoryGroupDto.from_category_group_model(product))
        return ShopApiResponse.success(result)
