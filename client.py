import requests
import re

"""

from urllib.parse import quote, unquote

# r = requests.get("http://localhost:8000/page/?a=11&b=23")

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

data = b"\x72\x84\x84\x80\x47\x49\x46\x49\x32\x49\x48\x49\x32\x83\x119\x105\x116\x99\x104\x105\x110\x103\x32\x80\x114\x111\x116\x111\x99\x111\x108\x115\x13\x10\x85\x112\x103\x114\x97\x100\x101\x58\x32\x119\x101\x98\x115\x111\x99\x107\x101\x116\x13\x10\x67\x111\x110\x110\x101\x99\x116\x105\x111\x110\x58\x32\x85\x112\x103\x114\x97\x100\x101\x13\x10\x83\x101\x99\x45\x87\x101\x98\x83\x111\x99\x107\x101\x116\x45\x65\x99\x99\x101\x112\x116\x58\x32\x115\x107\x111\x69\x80\x88\x72\x109\x121\x121\x66\x55\x90\x73\x50\x83\x110\x52\x51\x43\x77\x69\x79\x55\x84\x117\x77\x61\x13\x10\x13\x10".decode(
    "ascii"
)


print(data)

"""


r = requests.get(
    "http://localhost:8000",
    headers={"Connection": "Upgrade", "Sec-WebSocket-Key": "9Vx+wTgIFVnQWJRaxdtYoQ=="},
)

print(r.status_code)
print(r.content)


# Connection: Upgrade
# Cookie: _xsrf=2|239c7e35|4244b8edf3f99ad3d4b51f96f96a8bf4|1658684105; csrftoken=lsoHVA5p9Pcflazw6yBA98ZjOquH0muJaRsRoHw9lI3azYhiVGnoc6yyCGxoJSwa; sessionid=mi95erezfij9jbmrsggmy8zocbyx5onm
# Host: localhost:8000
# Origin: http://localhost:8000
# Pragma: no-cache
# Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
#
