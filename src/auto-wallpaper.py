#!/usr/bin/python

# -*- encode: utf-8 -*-

"""
auto-wallpaper

python-pip
pip requests
pip PIL
"""

import os
import sys
import time
import signal
import argparse
import syslog
import tempfile

import requests

from StringIO import StringIO




TIME_DELTA = 0.5
URL_RANDOM_IMAGE = 'http://fotobash.ru/random.php'
IS_RUN = True

def handler(signum, frame):
    global IS_RUN
    print 'Signal handler called with signal', signum
    IS_RUN = False


def get_image_url():
    r = requests.get(URL_RANDOM_IMAGE, stream=True)
    return str(r.content)


def save_image(url):
    file_ex = url.split('.')[-1]
    file_name = '/tmp/wallpaper.%s' % (file_ex,)

    r = requests.get(url, stream=True)
    fp = open(file_name, 'wb')
    fp.write(r.content)
    fp.close()

    return file_name


def set_wallpaper(file_name):
    os.system('gsettings set org.cinnamon.desktop.background picture-uri  "file:///%s"' % file_name)


def main():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    syslog.openlog( 'auto-wallpaper', 0, syslog.LOG_LOCAL4)

    syslog.syslog(syslog.LOG_INFO, 'start')
    
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--delay', help='Delay', type=int)

        delay = parser.parse_args().delay

        current_time = delay
        while IS_RUN:
            if current_time >= delay:
                url = get_image_url()
                file_name = save_image(url)
                set_wallpaper(file_name)

                syslog.syslog(syslog.LOG_INFO, 'change image')
                current_time = 0
            else:
                current_time += TIME_DELTA
                time.sleep(TIME_DELTA)
    except Exception as e:
        print e
        syslog.syslog(syslog.LOG_ERR, str(e))
        

    syslog.syslog(syslog.LOG_INFO, 'stop')
    
    syslog.closelog()

    sys.exit(0)

if __name__ == '__main__':
    main()