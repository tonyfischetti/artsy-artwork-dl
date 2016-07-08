#!/usr/bin/env python -tt

###########################################################
##                                                       ##
##   artsy-dl.py                                         ##
##                                                       ##
##                Author: Tony Fischetti                 ##
##                        tony.fischetti@gmail.com       ##
##                                                       ##
###########################################################


"""
this script is brittle
"""

__author__ = 'Tony Fischetti'
__version__ = '0.1'

import sys
import lxml.html
from lxml.cssselect import CSSSelector
import requests
import html2text as h2t
import re
import wget
import os




THE_URL = sys.argv[1]
FN_TEMPLATE = sys.argv[2]


ARTIST_CSS = CSSSelector(".entity-link")
TITLE_CSS = CSSSelector(".artwork-metadata__title em")
LINK_CSS = CSSSelector(".js-artwork-images__images__image__display__img")

ARTIST_REGEX = re.compile('\[(.+?)\]', re.UNICODE) 
TITLE_REGEX = re.compile('_(.+?)_, (\d+)', re.UNICODE) 
LINK_REGEX = re.compile('img data-src="(.+?)"')



def cop_out(f):
    def inner(*args, **kargs):
        try:
            return f(*args, **kargs)
        except Exception as e:
            print("The function <{}> failed".format(f.__name__))
            sys.exit(1)
    return inner


@cop_out
def get_text_from_element(element):
    return h2t.html2text(lxml.html.tostring(element).decode("utf-8")).rstrip()


@cop_out
def get_tree(url):
    r = requests.get(url)
    return lxml.html.fromstring(r.text)


@cop_out
def get_artist(tree):
    artist_text = get_text_from_element(ARTIST_CSS(tree)[0])
    final_artist = ARTIST_REGEX.search(artist_text).group(1)
    return final_artist


@cop_out
def get_title_and_date(tree):
    title_text = get_text_from_element(TITLE_CSS(tree)[0])
    tmp = TITLE_REGEX.search(title_text)
    return tmp.group(1), tmp.group(2)


@cop_out
def get_link(tree):
    link_text = lxml.html.tostring(LINK_CSS(tree)[0]).decode("utf-8")
    final_link = LINK_REGEX.search(link_text).group(1)
    return final_link


@cop_out
def get_new_filename(artist, title, date):
    template = FN_TEMPLATE
    if "%a" in FN_TEMPLATE:
        template = template.replace("%a", artist)
    if "%t" in FN_TEMPLATE:
        template = template.replace("%t", title)
    if "%d" in FN_TEMPLATE:
        template = template.replace("%d", date)
    return template


@cop_out
def download_image(link):
    old_filename = wget.download(link)
    return old_filename


@cop_out
def rename_downloaded_image(old_filename, artist, title, date):
    tmp, extension = os.path.splitext(old_filename)
    new_filename = get_new_filename(artist, title, date)
    os.rename(old_filename, "{}{}".format(new_filename, extension))
    return True



def main():
    tree = get_tree(THE_URL)

    artist = get_artist(tree)
    title, date = get_title_and_date(tree)
    link = get_link(tree)

    old_filename = download_image(link)
    rename_downloaded_image(old_filename, artist, title, date)





if __name__ == '__main__':
    STATUS = main()
    sys.exit(STATUS)

