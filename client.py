import requests
import re

from urllib.parse import quote, unquote

r = requests.get("http://localhost:8000/page/?a=11&b=23")

# r = requests.post("http://localhost:8000/page/", data={"name": "gio", "age": 29})


req = [
    "GET /page/?page=12&ab=12#dgdfg HTTP/1.1",
    "Host: localhost:8000",
    "Connection: keep-alive",
    "Cache-Control: max-age=0",
    "Upgrade-Insecure-Requests: 1",
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
    "Accept-Language: en-US",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-GPC: 1",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-User: ?1",
    "Sec-Fetch-Dest: document",
    "Accept-Encoding: gzip, deflate, br",
    "Cookie: csrftoken=1Mui9kkdtVnqCgkolj9LQXk9vAjurufoNg9gr7r54ifoA1GlrdZ7LCFvxIeZp0rE; _xsrf=2|239c7e35|4244b8edf3f99ad3d4b51f96f96a8bf4|1658684105",
    "",
    "",
]

# req_info_praser = re.compile(r"(?P<method>[A-Z]+)\s(?P<url>.*?(?=\s))")
# req_info = req_info_praser.search(req[0])

# method = req_info.group("method")
# url = req_info.group("url")

# print(method)
# print(url)

# print(quote("/my+page/.dsf;/?page=12&page=23"))


# ampersand ("&")
# dollar ("$")
# plus sign ("+")
# comma (",")
# forward slash ("/")
# colon (":")
# semi-colon (";")
# equals ("=")
# question mark ("?")
# 'At' symbol ("@")
# pound ("#").
