#!/usr/bin/env python3

'''Check list of files and determine which one to unzip'''

import datetime as dt


def main():
    file_list = {'2016/08/06': 'filexx.zip',
                 '2016/08/25': 'filexy.zip',
                 '2016/08/26': 'filexz.zip'}

    current_date = dt.date.today().strftime('%Y/%m/%d')

    try:
        target_file = file_list[current_date]
    except KeyError:
        print('No matching files for today')
        return None

    # FTP into server and unzip file
    #           OR
    # Unzip file locally and upload onto FTP server
    # whatever one is easier


if __name__ == '__main__':
    main()
