import re
import socket
from http import HTTPStatus
from urllib.parse import quote, unquote, urlparse, parse_qs

LINE_BREAK = b"\r\n"
CONTENT_SEPARATOR = LINE_BREAK * 2


class HttpRequest:
    def __init__(self, client_connection: socket) -> None:
        body: bytes = client_connection.recv(1024)

        info_ind = body.find(LINE_BREAK)
        head_ind = body.find(CONTENT_SEPARATOR)

        info = body[:info_ind].strip().decode()
        header = body[info_ind:head_ind].strip().decode()
        content = body[head_ind:].strip()

        self._parse_info(info)
        self._parse_header(header)
        self._parse_content(content)

    def _parse_info(self, info: str):
        parser = re.compile(r"(?P<method>[A-Z]+)\s(?P<url>.*?(?=\s))")

        data = parser.search(info)

        self.method = data.group("method")
        self.url = data.group("url")

    def _parse_header(self, header: str):
        self.headers = {}

        for head in header.split("\n"):
            key, value = head.split(":", 1)
            self.headers[key.strip()] = value.strip()

    def _parse_content(self, content: bytes):
        return


class HttpResponse:
    def __init__(
        self, content, content_type="text/html", status: HTTPStatus = HTTPStatus.OK
    ) -> None:

        response = [f"HTTP/1.1 {status.value} {status.name}"]

        response.append("\n")

        response.append(content)

        self.response = response

    def to_bytes(self):

        return self.response


class Server:
    def __init__(self, socket_address) -> None:
        self.SERVER_HOST, self.SERVER_PORT = socket_address

        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(socket_address)
        self.socket.listen(1)

    def run(self):

        print("Listening on port %s ...\n\n" % self.SERVER_PORT)

        while True:
            try:
                client_connection, client_address = self.socket.accept()

                try:
                    request: HttpRequest = self.handle_request(client_connection)

                    print(f"Reqested: {request.method} on address {request.url}")
                    print()

                except Exception:
                    badreq = HTTPStatus.BAD_REQUEST
                    response = f"HTTP/1.1 {badreq.value} {badreq.name}\n\nBad Request"
                    client_connection.sendall(response.encode())
                    client_connection.close()

                # Send HTTP response
                self.handle_response(client_connection)

            except KeyboardInterrupt:
                break

        # Close socket
        self.socket.close()

    def handle_request(self, client_connection: socket) -> HttpRequest:

        req = HttpRequest(client_connection)

        return req

    def handle_response(self, client_connection: socket):
        with open("./index.html", "rb") as fp:
            content = fp.read()

        response = b"HTTP/1.0 200 OK" + CONTENT_SEPARATOR + content
        client_connection.sendall(response)
        client_connection.close()


if __name__ == "__main__":

    server = Server(("127.0.0.1", 8000))
    server.run()
