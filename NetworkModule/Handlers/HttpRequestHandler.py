from http.server import BaseHTTPRequestHandler

from JsonFomatterModule.JsonFormatter import JsonFormatter
from NetworkModule.Data.ExceptionsData.ServerLogicException import ServerLogicException
from NetworkModule.Handlers.MethodHandler import MethodHandler


# noinspection PyPep8Naming
class HttpRequestHandler(BaseHTTPRequestHandler):
    method_handler: MethodHandler

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.__send_options_header()

    def do_GET(self):
        method_name = MethodHandler.get_server_method_name(self.path)

        try:
            response_dto = HttpRequestHandler.method_handler.do_get(method_name)
        except ServerLogicException as ex:
            self.send_error(ex.state_code, ex.message)
            return

        self.send_response(response_dto.state_code)
        self.__send_header()

        response_dto_json = JsonFormatter.serialize(response_dto)
        self.wfile.write(response_dto_json.encode())

    def do_POST(self):
        length: int = int(self.headers.get('content-length', 0))
        json_request_dto: str = self.rfile.read(length).decode("utf-8")
        method_name = MethodHandler.get_server_method_name(self.path)

        try:
            request_dto = HttpRequestHandler.method_handler.get_request_dto(json_request_dto, method_name,
                                                                            self.client_address)
            response_dto = HttpRequestHandler.method_handler.do_post(method_name, request_dto)
        except ServerLogicException as ex:
            self.send_error(ex.state_code, ex.message)
            return

        response_dto_json = JsonFormatter.serialize(response_dto)

        self.send_response(response_dto.state_code)
        self.__send_header()

        self.wfile.write(response_dto_json.encode())

    def __send_options_header(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def __send_header(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
