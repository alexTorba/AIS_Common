from JsonFomatterModule.JsonContract import JsonContract
from JsonFomatterModule.JsonFormatter import JsonFormatter
from NetworkModule.Data.DtoData.RequestData.RequestDto import RequestDto
from NetworkModule.Managers.NetworkManager import NetworkManager


class GetKeysByAuditoriumDto(JsonContract):
    auditorium: str
    __json_fields = {
        "a": "auditorium"
    }

    def __init__(self, auditorium=None):
        super().__init__(self.__json_fields)
        if auditorium is not None:
            self.auditorium = auditorium


class SendRequestTest:
    # noinspection SpellCheckingInspection
    @staticmethod
    def use_unsupported_server_method():
        # GET request
        result = NetworkManager.get("GetAuditor")
        print(result)

        # POST request
        dto = RequestDto[GetKeysByAuditoriumDto](data=GetKeysByAuditoriumDto("39"))
        json = JsonFormatter.serialize(dto)
        result = NetworkManager.send("GetKeysByAuditori", json)
        print(result)

    @staticmethod
    def send_wrong_dto():
        # wrong dto. Might be RequestDto[ComputerKey]
        dto = RequestDto[GetKeysByAuditoriumDto](data=GetKeysByAuditoriumDto("39"))
        json = JsonFormatter.serialize(dto)
        result = NetworkManager.send("GetComputer", json)
        print(result)

        json_dto = '{"d": {"a": 3}}'  # type value of "a" might be a string
        result2 = NetworkManager.send("GetComputer", json_dto)
        print(result2)

    @staticmethod
    def get_keys_by_auditorium():
        dto = RequestDto[GetKeysByAuditoriumDto](data=GetKeysByAuditoriumDto("39"))
        json = JsonFormatter.serialize(dto)
        result = NetworkManager.send("GetKeysByAuditorium", json)
        print(result)


if __name__ == '__main__':
    SendRequestTest.get_keys_by_auditorium()
