from common.controllers import AnonymousView, ShopApiResponse
from shop_api.auth.dto import SignInDto
from django.contrib.auth import authenticate, login, logout

__author__ = 'artem'


class SignInController(AnonymousView):
    def post(selfself, request):
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

