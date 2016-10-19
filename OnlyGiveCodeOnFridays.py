import datetime
import re
import hashlib
import binascii

salt = 5618418165421843546546436546463546984 #just random gibberish I typed in

now_date = datetime.datetime.today().date()
time_to_fri = datetime.timedelta((11 - now_date.weekday()) % 7)
next_friday = now_date + time_to_fri
next_code = int(next_friday.strftime('%m')) + int(next_friday.strftime('%d'))

'''Im sure theres a more elegant way of doing the following, effectively what I'm trying to do is have a reproducable code, but that can't be guessed'''
new_pw = hashlib.pbkdf2_hmac('sha256', b'next_code', b'salt', 100000)
new_pw = binascii.hexlify(new_pw)
new_pw = re.findall(r'\d+', str(new_pw))
new_pw = "".join(new_pw)
new_pw = new_pw[-5:]

now_day = datetime.datetime.today().weekday()

if now_day == 4:
    print("New password: {0}".format(new_pw))
else:
    print("Not yet nigga")