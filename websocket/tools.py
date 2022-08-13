import re
import socket
from base64 import b64encode
from hashlib import sha1
from http import HTTPStatus
from urllib.parse import parse_qs, unquote, urlparse

from .const import CONTENT_SEPARATOR, LINE_BREAK, SEC_WEBSOCKET_KEY


class Url:

    __slots__ = ("schema", "netloc", "path", "params", "fragment", "query")

    def __init__(self, url) -> None:
        parsed = urlparse(unquote(url))

        self.schema = parsed.scheme
        self.netloc = parsed.netloc
        self.path = parsed.path
        self.params = parsed.params
        self.fragment = parsed.fragment
        self.query = parse_qs(parsed.query)


class HttpRequest:
    def __init__(self, client_connection: socket.socket) -> None:
        body: bytes = client_connection.recv(1024)

        self._body = body

        if not body:
            return

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
        self.url = Url(data.group("url"))

    def _parse_header(self, header: str):
        self.headers = {}

        for head in header.split("\n"):
            key, value = head.split(":", 1)
            self.headers[key.strip()] = value.strip()

    def _parse_content(self, content: bytes):
        return

    def is_valid(self):
        return len(self._body) > 0


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


def create_socket_accept_key(sec_websocket_key: str) -> bytes:
    key = sha1((sec_websocket_key + SEC_WEBSOCKET_KEY).encode())

    return b64encode(key.digest())


def prepare_handshake_headers(sec_websocket_key: str):
    accept_key = create_socket_accept_key(sec_websocket_key)

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
