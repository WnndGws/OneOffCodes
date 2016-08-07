#!/usr/bin/env python3

'''Check list of files and determine which one to unzip'''

import datetime as dt
import os


def main():
    file_list = {'2016/08/07': 'filexx.z',
                 '2016/08/25': 'filexy.z',
                 '2016/08/26': 'filexz.z'}

    current_date = dt.date.today().strftime('%Y/%m/%d')

    try:
        target_file = file_list[current_date]
        os.system('7z x {0} {1}'.format(target_file, target_file.split(".", 1)[0])
    except KeyError:
        print('No matching files for today')
        return None

    # FTP into server and unzip file (EASIER OPTION)
    #           OR
    # Unzip file locally and upload onto FTP server
    # whatever one is easier


#if __name__ == '__main__':
#    main()
