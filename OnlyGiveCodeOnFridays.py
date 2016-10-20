import binascii
import datetime as dt
import hashlib
import re

salt = b'5618418165421843546546436546463546984'  # byte-string of random numbers

now_date = dt.date.today()
time_to_fri = dt.timedelta((4 - now_date.weekday()) % 7)
next_friday = now_date + time_to_fri
next_code = next_friday.strftime('%m') + next_friday.strftime('%d')

# Produce a unique 5 digit passcode
# step one: calculate SHA256 hash (bytes string)
new_pw = hashlib.pbkdf2_hmac('sha256', next_code.encode(), salt, 100000)
# step two: convert each char of the byte string to its hexadecimal notation (bytes string)
new_pw = binascii.hexlify(new_pw)
# step three: remove non-numeric parts of the string
new_pw = re.findall(r'\d+', new_pw.decode())
new_pw = "".join(new_pw)
# step four: take the passcode from the first 5 digits
new_pw = new_pw[-5:]

if now_date.weekday() == 4:
    print("New password: {0}".format(new_pw))
else:
    print("Not yet nigga")
