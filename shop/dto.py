from rest_framework.fields import empty
from rest_framework.serializers import Serializer
__author__ = 'artem'


class ShopBaseDto(Serializer):

    def to_dict(self):
        if not hasattr(self, '_data'):
            return self.initial_data
        else:
            return self.data

    def __init__(self, data=empty, **kwargs):
        self.initial_data = {}
        super(ShopBaseDto, self).__init__(None, data, **kwargs)

    def __setattr__(self, key, value):
        if key in self.get_declared_fields():
            self.initial_data[key] = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.get_declared_fields():
            return self.initial_data.get(key)
        else:
            if key in dir(super(ShopBaseDto, self)):
                return getattr(super(), key)
            else:
                raise AttributeError("Object {} doesn't have attribute {}".format(self.__class__.__name__, key))

    @classmethod
    def from_dict(cls, dictionary=empty):
        instance = cls(dictionary)
        return instance

    @classmethod
    def get_declared_fields(cls):
        if hasattr(cls, '_declared_fields'):
            return getattr(cls, '_declared_fields')
        else:
            return []


class ShopApiResponseServiceSection(ShopBaseDto):

    def __init__(self):
        self.error_code = 0
        self.error_message = None
        self.validation_errors = []

    def is_successful(self):
        return self.error_code == 0

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "error_message": self.error_message,
            "validation_errors": self.validation_errors,
            "successful": self.is_successful()
        }


class ShopApiResponseDto(ShopBaseDto):

    def __init__(self, payload=None):
        self.payload = payload
        self.service = ShopApiResponseServiceSection()

    def to_dict(self):
        serialized_payload = self.payload
        if isinstance(self.payload, ShopBaseDto):
            serialized_payload = self.payload.to_representation(self.payload)
        return {
            "payload": serialized_payload,
            "service": self.service.to_dict()
        }