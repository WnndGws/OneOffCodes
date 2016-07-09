from grab import Grab

g = Grab()

g.go('http://192.168.0.1/html/reboot.html')
g.doc.set_input('username', 'admin')
g.doc.set_input('password', '*********')
g.doc.submit()
