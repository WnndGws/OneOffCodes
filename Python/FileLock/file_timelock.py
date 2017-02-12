#!/usr/bin/env python3

"""Check list of files and determine which one to unzip"""

import datetime as dt
import os
import pickle

file_list = {}
state = 'inputting'
while state == 'inputting':
    state = input('Would you like to enter another file? (Y/n): ')
    if state.lower() in ('yes', '', 'y'):
        state = 'inputting'
    else:
        state = 'brokk'
        break
    file_input = input('Enter a file you would like to unzip and the date (Filename - yyyymmdd): ')
    file_name = str(file_input.split(" - ", 1)[0])
    file_date = str(file_input.split(" - ", 1)[1])
    file_list[file_date] = file_name
    with open('filelock.settings', 'wb') as file:
        pickle.dump(file_list, file, protocol=pickle.HIGHEST_PROTOCOL)

current_date = dt.date.today().strftime('%Y%m%d')

with open('filelock.settings', 'rb') as file:
    file_list = pickle.load(file)

try:
    target_file = file_list[current_date]
    os.system('7z x {0}'.format(target_file))
except KeyError:
    print('No matching files for today')

    # FTP into server and unzip file (EASIER OPTION)
    #           OR
    # Unzip file locally and upload onto FTP server
    # whatever one is easier


    # if __name__ == '__main__':
    #    main()
