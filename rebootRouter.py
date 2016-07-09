from grab import Grab

g = Grab()
pw = input('What is your password? ')

g.go('http://192.168.0.1/html/reboot.html')
g.doc.set_input('username', 'admin')
g.doc.set_input('password', pw)
g.doc.submit()
