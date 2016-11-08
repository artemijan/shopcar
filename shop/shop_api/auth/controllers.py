from shop_core.common.controllers import AnonymousView, ShopApiResponse
from shop_core.common.errors import SaveEntityError
from shop_core.services.account_service import create_account
from shop_api.auth.dto import SignInDto, SignUpDto, UserDto
from django.contrib.auth import authenticate, login, logout

__author__ = 'artem'


class SignInController(AnonymousView):
    def post(self, request):
        dto = SignInDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        user = authenticate(username=dto.username, password=dto.password)
        if user is None:
            return ShopApiResponse.bad_request("Invalid credentials")
        if not user.is_active:
            return ShopApiResponse.bad_request("Inactive user")
        login(request, user)
        # todo return users dto back to client
        return ShopApiResponse.success({})


class SignOutController(AnonymousView):
    def post(self, request):
        logout(request)
        return ShopApiResponse.success("Logged out")


class SignUpController(AnonymousView):
    def post(self, request):
        dto = SignUpDto.from_dict(request.data)
        if not dto.is_valid():
            return ShopApiResponse.bad_request(dto)
        try:
            create_account(
                username=dto.username,
                email=dto.email,
                password=dto.password,
                first_name=dto.first_name,
                last_name=dto.last_name
            )
        except SaveEntityError as e:
            return ShopApiResponse.bad_request(str(e))
        user = authenticate(username=dto.username, password=dto.password)
        login(request, user)
        user_dto = UserDto.from_account_model(user)
        return ShopApiResponse.success(user_dto)
