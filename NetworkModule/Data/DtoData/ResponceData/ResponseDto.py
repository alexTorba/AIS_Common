import typing
from typing import TypeVar

from JsonFomatterModule.JsonContract import JsonContract
from NetworkModule.Data.DtoData.ResponceData.BaseResponseDto import BaseResponseDto

T = TypeVar("T", bound=JsonContract)


class ResponseDto(BaseResponseDto, typing.Generic[T]):
    data: T
    __json_field = {"d": "data"}

    def __init__(self, status_code: int = None, data: T = None):
        super().__init__(status_code)

        if data is not None:
            self.data = data
        self._update_json_fields(self.__json_field)
