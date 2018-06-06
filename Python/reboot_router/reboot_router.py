import urllib.request
from bs4 import BeautifulSoup

url = "http://192.168.0.1/html/reboot.html"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
username = "admin"
password = input("Password? ")

manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
manager.add_password(None, url, username, password)

handler = urllib.request.HTTPBasicAuthHandler(manager)

opener = urllib.request.build_opener(handler)
opener.open(url)
urllib.request.install_opener(opener)

req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as response:
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())
