import logging
import re
import select
import socket
import threading
import pathlib
from http import HTTPStatus
from typing import List, Set, Tuple

from .const import CONTENT_SEPARATOR
from .tools import (
    HttpRequest,
    prepare_handshake_headers,
)

logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

base_dir = pathlib.Path(__file__).resolve().parent.parent


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.host, self.port = addr

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(addr)
        self.server_socket.setblocking(False)

    def close_client(self, client: socket.socket):
        client.close()
        self.readers.remove(client)

    def run(self):

        self.server_socket.listen(2)

        self.readers = [self.server_socket]

        while self.readers:
            try:
                # logging.info("Socket - waiting...")
                readable, writable, exceptional = select.select(
                    self.readers, [], self.readers, 0.5
                )

                readable: List[socket.socket]
                writable: List[socket.socket]
                exceptional: List[socket.socket]

                for s in readable:
                    try:
                        if s == self.server_socket:
                            client, addr = s.accept()
                            client.setblocking(False)
                            self.readers.append(client)
                            logging.info(f"Connection: {addr}")
                        else:
                            self.handle_client_socket(s)
                    except Exception as ex:
                        logging.warning(str(ex))
                    finally:
                        pass

                for s in exceptional:
                    logging.info("Non Blocking - error")
                    self.readers.remove(s)
                    break
            except KeyboardInterrupt:
                break

    def handle_client_socket(self, client: socket.socket):

        request = HttpRequest(client)

        if not request.is_valid():
            logging.info(f"Remove: {client}")
            self.close_client(client)
            return

        logging.info(f"Echo: {request._body}")

        connection = request.headers.get("Connection", "")

        if connection == "Upgrade":
            self.handle_connection_upgrade(request, client)
        else:
            self.handle_http_request(request, client)

    def handle_http_request(self, request: HttpRequest, client: socket.socket):
        content = (base_dir / "public/index.html").read_bytes()
        response = b"HTTP/1.1 200 OK" + CONTENT_SEPARATOR + content
        client.sendall(response)
        self.close_client(client)

    def handle_connection_upgrade(self, request: HttpRequest, client: socket.socket):

        sec_websocket_key = request.headers["Sec-WebSocket-Key"]

        logging.info(f"\n\n{sec_websocket_key} is connected...")

        headers = prepare_handshake_headers(sec_websocket_key)
        logging.info(f"\n\nHEADERS: {headers}")

        client.sendall(headers)

        # self.close_client(client)
