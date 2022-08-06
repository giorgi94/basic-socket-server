import requests
import re

from urllib.parse import quote, unquote

r = requests.get("http://localhost:8000/page/?a=11&b=23")

b"GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: Upgrade\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36\r\nUpgrade: websocket\r\nOrigin: http://localhost:8000\r\nSec-WebSocket-Version: 13\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: csrftoken=1Mui9kkdtVnqCgkolj9LQXk9vAjurufoNg9gr7r54ifoA1GlrdZ7LCFvxIeZp0rE; _xsrf=2|239c7e35|4244b8edf3f99ad3d4b51f96f96a8bf4|1658684105\r\nSec-WebSocket-Key: mqCIzcnwN8/nJ/ldblBEdw==\r\nSec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n\r\n"


{
    "Host": "localhost:8000",
    "Connection": "Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
    "Upgrade": "websocket",
    "Origin": "http://localhost:8000",
    "Sec-WebSocket-Version": "13",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "csrftoken=1Mui9kkdtVnqCgkolj9LQXk9vAjurufoNg9gr7r54ifoA1GlrdZ7LCFvxIeZp0rE; _xsrf=2|239c7e35|4244b8edf3f99ad3d4b51f96f96a8bf4|1658684105",
    "Sec-WebSocket-Key": "9HDQlRYwUgvjy3ApK8U2BQ==",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
}
