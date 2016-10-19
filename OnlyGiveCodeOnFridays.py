import binascii
import datetime as dt
import hashlib
import re

salt = '5618418165421843546546436546463546984' #just random gibberish I typed in

now_date = dt.date.today()
time_to_fri = dt.timedelta((4 - now_date.weekday()) % 7)
next_friday = now_date + time_to_fri
next_code = next_friday.strftime('%m') + next_friday.strftime('%d')

'''Im sure theres a more elegant way of doing the following, effectively what I'm trying to do is have a reproducable code, but that can't be guessed'''
new_pw = hashlib.pbkdf2_hmac('sha256', next_code.encode(), salt.encode(), 100000)
new_pw = binascii.hexlify(new_pw)
new_pw = re.findall(r'\d+', str(new_pw))
new_pw = "".join(new_pw)
new_pw = new_pw[-5:]

# for debugging
# print(new_pw)

if now_date.weekday() == 4:
    print("New password: {0}".format(new_pw))
else:
    print("Not yet nigga")