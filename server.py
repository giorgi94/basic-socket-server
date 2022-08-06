import re
import select
import socket
from base64 import b64decode, b64encode
from hashlib import sha1
from http import HTTPStatus
from typing import Set
from urllib.parse import parse_qs, quote, unquote, urlparse

LINE_BREAK = b"\r\n"
CONTENT_SEPARATOR = LINE_BREAK * 2

SEC_WEBSOCKET_KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B1"


# b64encode: to base64


class HttpRequest:
    def __init__(self, client_connection: socket) -> None:
        body: bytes = client_connection.recv(1024)

        self._body = body

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

        self.clients: Set[socket.socket] = set()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(socket_address)

        self.socket.listen(5)

    def run(self):
        print("Listening on port %s ...\n\n" % self.SERVER_PORT)

        self.sockets_list = [self.socket]

        while True:
            try:
                read_sockets, _, exception_sockets = select.select(
                    self.sockets_list, [], self.sockets_list
                )

                for notified_socket in read_sockets:
                    if notified_socket == self.socket:
                        client_socket, client_address = self.socket.accept()

                        try:
                            closed = self.handle_request(client_socket)
                        except Exception as error:
                            print("ERROR:", error)
                            return self.send_bad_request(client_socket)

                        if closed:
                            continue

                        self.sockets_list.append(client_socket)
                        self.clients.add(client_socket)
                    else:
                        print("\n\nClient: ", notified_socket)

                for notified_socket in exception_sockets:
                    self.sockets_list.remove(notified_socket)
                    self.clients.remove(notified_socket)
            except Exception as err:
                print("Error (2):", err)
                break
            except KeyboardInterrupt:
                break

        self.socket.close()

    def handle_request(self, client: socket.socket) -> False:

        request = HttpRequest(client)

        print(client, request._body.decode())
        print("---\n\n")

        connection = request.headers.get("Connection", "")

        if connection == "Upgrade":
            self.upgrade(request, client)
            return False

        # handlers = {"GET": self.get, "POST": self.post}

        self.get(request, client)

        return True

    def close_client(self, client):
        client.close()

        if client in self.clients:
            self.clients.remove(client)

    def send_bad_request(self, client: socket.socket):
        badreq = HTTPStatus.BAD_REQUEST
        response = f"HTTP/1.1 {badreq.value} {badreq.name}\n\nBad Request"
        client.sendall(response.encode())

        self.close_client(client)

    def get(self, request: HttpRequest, client: socket.socket) -> HttpResponse:

        with open("./public/index.html", "rb") as fp:
            content = fp.read()

        response = b"HTTP/1.0 200 OK" + CONTENT_SEPARATOR + content
        client.sendall(response)

        self.close_client(client)

    def post(self, request: HttpRequest, client: socket.socket) -> HttpResponse:
        return

    def upgrade(self, request: HttpRequest, client: socket.socket):

        is_websocket = request.headers.get("Upgrade") == "websocket"

        if not is_websocket:
            return self.send_bad_request(client)

        sec_websocket_key = request.headers["Sec-WebSocket-Key"]

        print(f"{sec_websocket_key} is connected...")

        headers = self.prepare_handshake_headers(sec_websocket_key)

        print(headers.decode())

        client.sendall(headers)
        client.close()

    def create_socket_accept_key(self, sec_websocket_key: str) -> bytes:
        key = sha1((sec_websocket_key + SEC_WEBSOCKET_KEY).encode())

        return b64encode(key.digest())

    def prepare_handshake_headers(self, sec_websocket_key: str):
        accept_key = self.create_socket_accept_key(sec_websocket_key)

        headers = (
            LINE_BREAK.join(
                [
                    b"HTTP/1.1 101 Switching Protocols",
                    b"Upgrade: websocket",
                    b"Connection: Upgrade",
                    b"Sec-WebSocket-Accept: " + accept_key,
                ]
            )
            + LINE_BREAK
        )

        return headers


if __name__ == "__main__":

    server = Server(("127.0.0.1", 8000))
    server.run()
