import urllib.request

url = 'http://192.168.0.1/html/reboot.html'
username = 'admin'
password = input("Password? ")

auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='', uri=url, user=username, passwd=password)
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
f = urllib.request.urlopen(url)
print(f.status)
print(f.reason)
print(f.read().decode('utf-8'))