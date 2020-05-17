from typing import Union, Callable, Dict, Tuple

from JsonFomatterModule.JsonFormatter import JsonFormatter
from NetworkModule.Data.DtoData.RequestData.BaseRequestDto import BaseRequestDto
from NetworkModule.Data.DtoData.ResponceData.BaseResponseDto import BaseResponseDto
from NetworkModule.Data.ExceptionsData.ServerLogicException import ServerLogicException
from NetworkModule.Managers.UrlManager import UrlManager


class MethodHandler:
    __method_handler: Dict[str, Union[Callable[[], BaseResponseDto], Callable[[BaseRequestDto], BaseResponseDto]]]

    def __init__(self, method_handler: dict):
        self.__method_handler = method_handler

    def do_get(self, server_method: str) -> BaseResponseDto:
        handler = self.__method_handler.get(server_method, None)
        if handler is None:
            raise ServerLogicException(400, f"Unsupported server method {server_method}!")
        return handler()

    def do_post(self, server_method: str, dto: BaseRequestDto):
        return self.__method_handler[server_method](dto)

    def get_request_dto(self, json_request_dto: str,
                        method_name: str,
                        client_address: Tuple[str, int]) -> BaseRequestDto:
        dto_type = self.__get_request_type(method_name)
        request_dto = JsonFormatter.deserialize(json_request_dto, dto_type)

        if not hasattr(request_dto, "data"):
            raise ServerLogicException(400, f"Server work only with dto types ! Stop spam !")

        UrlManager.resolve_client_address(request_dto, client_address)
        return request_dto

    # noinspection PyUnresolvedReferences
    def __get_request_type(self, server_method: str):
        handler = self.__method_handler.get(server_method, None)
        if handler is None:
            raise ServerLogicException(400, f"Unsupported server method {server_method}!")
        return handler.__annotations__["dto"]

    @staticmethod
    def get_server_method_name(request_path: str) -> str:
        return request_path[1:]
