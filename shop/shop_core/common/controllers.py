import collections
from dto import ShopBaseDto, ShopApiResponseDto
from errors import InvalidPaginationOptionsError
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.settings import api_settings
from json import JSONEncoder
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status as HttpStatus
from rest_framework.permissions import IsAuthenticated

__author__ = 'artem'


class ShopApiResponse(Response):
    __SECRET = object()
    HttpStatus = HttpStatus

    def __init__(self, payload=None, status=None, template_name=None, headers=None, exception=False,
                 content_type='application/json',
                 secret=None):
        if secret != self.__SECRET:
            raise ValueError(
                "Using constructor of the ShopApiResponse is not allowed, please "
                "use static methods instead. See .success()")

        assert payload is None \
               or isinstance(payload, collections.Iterable) \
               or isinstance(payload, ShopBaseDto), "payload should be subclass of ShopBaseDto"
        super().__init__(None, status, template_name, headers, exception, content_type)
        api_response_dto = ShopApiResponseDto(payload)
        self.data = api_response_dto

    @classmethod
    def not_found(cls, dto_or_error_message, error_code=None):
        response = ShopApiResponse(None, status=cls.HttpStatus.HTTP_404_NOT_FOUND, secret=cls.__SECRET)
        if isinstance(dto_or_error_message, ShopBaseDto):
            response.data.service.validation_errors = dto_or_error_message.errors
        response.data.service.error_code = error_code if error_code is not None else response.status_code
        response.data.service.error_message = "Entity not found" \
            if isinstance(dto_or_error_message, ShopBaseDto) else str(dto_or_error_message)
        return response

    @classmethod
    def success(cls, payload, status=HttpStatus.HTTP_200_OK):
        return ShopApiResponse(payload, status=status, secret=cls.__SECRET)

    @classmethod
    def not_authenticated(cls, *args):
        response = ShopApiResponse(None, status=cls.HttpStatus.HTTP_401_UNAUTHORIZED, secret=cls.__SECRET)
        if len(args) > 0:
            message = args[0]
        else:
            message = "Unauthorized"
        response.data.service.error_message = message
        return response

    @classmethod
    def bad_request(cls, dto_or_error_message, error_code=None):
        response = ShopApiResponse(None, status=cls.HttpStatus.HTTP_400_BAD_REQUEST, secret=cls.__SECRET)
        if isinstance(dto_or_error_message, ShopBaseDto):
            response.data.service.validation_errors = dto_or_error_message.errors
        response.data.service.error_code = error_code if error_code is not None else response.status_code
        response.data.service.error_message = "Bad request. Check service.validation_errors for details" \
            if isinstance(dto_or_error_message, ShopBaseDto) else str(dto_or_error_message)
        return response

    @classmethod
    def internal_server_error(cls, exception):
        response = ShopApiResponse(None, status=cls.HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, secret=cls.__SECRET)
        response.data.service.error_code = cls.HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
        return response


class ShopJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ShopBaseDto):
            return o.to_dict()
        else:
            return super().default(o)


class JsonRenderer(JSONRenderer):
    encoder_class = ShopJsonEncoder
    media_type = 'application/json'
    format = 'json'
    ensure_ascii = not api_settings.UNICODE_JSON
    compact = api_settings.COMPACT_JSON

    def get_indent(self, accepted_media_type, renderer_context):
        return None if self.compact else 4

    def render(self, api_response, accepted_media_type=None, renderer_context=None):
        # assert isinstance(api_response, ShopApiResponseDto), "api_response should be an instance of ShopApiResponseDto"
        return super().render(api_response, accepted_media_type, renderer_context)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class PaginationOptions(object):
    """ Pagination options class, has offset and limit parameters."""

    def __init__(self, offset=0, limit=50):
        """ Return pagination options object with limit and offset.

        :param offset: Pagination offset
        :type offset: int
        :param limit: Pagination limit
        :type limit: int
        :rtype: PaginationOptions
        """
        self.offset = offset
        self.limit = limit


class AnonymousView(APIView):
    renderer_classes = [JsonRenderer]
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pagination_options = None

    @property
    def pagination_options(self):
        if self._pagination_options is None:
            try:
                offset = int(self.request.GET.get('offset', '0'))
                limit = int(self.request.GET.get('limit', '50'))
                self._pagination_options = PaginationOptions(offset=offset, limit=limit)
            except ValueError:
                raise InvalidPaginationOptionsError('Bad offset and/or limit')
        return self._pagination_options


class ShopApiView(AnonymousView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


def shop_exception_handler(exc, context):
    if isinstance(exc, InvalidPaginationOptionsError):
        return ShopApiResponse.bad_request('Bad limit and/or offset')
