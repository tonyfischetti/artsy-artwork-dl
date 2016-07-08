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
Downloads artwork from artsy.net (from a URL given as a
CLI argument) and renames the downloaded file to follow
a filename template (given as a CLI arg) based on the
artist's name, the title of the piece, and the date of
completion.
"""

__author__ = 'Tony Fischetti'
__version__ = '0.2'

import os
import re
import sys

import html2text as h2t
import lxml.html
from lxml.cssselect import CSSSelector
import requests
import wget


ARTIST_CSS = CSSSelector(".entity-link")
TITLE_CSS = CSSSelector(".artwork-metadata__title em")
LINK_CSS = CSSSelector(".js-artwork-images__images__image__display__img")

ARTIST_REGEX = re.compile('\[(.+?)\]', re.UNICODE)
TITLE_REGEX = re.compile('_(.+?)_, (\d+)', re.UNICODE)
LINK_REGEX = re.compile('img data-src="(.+?)"', re.UNICODE)
SEP_DIRS = re.compile("^(.+)/(.+?)$", re.UNICODE)


#--------------------------------------------------#
def cop_out(f):
    def inner(*args, **kargs):
        try:
            return f(*args, **kargs)
        except:
            message = f.__name__.replace("_", " ")
            sys.exit("\nFailed to {}\n".format(message))
    return inner
#--------------------------------------------------#


@cop_out
def get_command_line_arguments():
    return sys.argv[1], sys.argv[2]


@cop_out
def download_webpage(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception
    return r


@cop_out
def parse_webpage(requests_object):
    return lxml.html.fromstring(requests_object.text)


@cop_out
def extract_text_from_element(element):
    return h2t.html2text(lxml.html.tostring(element).decode("utf-8")).rstrip()


@cop_out
def extract_artist_name_from_webpage(tree):
    artist_text = extract_text_from_element(ARTIST_CSS(tree)[0])
    return ARTIST_REGEX.search(artist_text).group(1)


@cop_out
def extract_title_and_date_from_webpage(tree):
    title_text = extract_text_from_element(TITLE_CSS(tree)[0])
    tmp = TITLE_REGEX.search(title_text)
    return tmp.group(1), tmp.group(2)


@cop_out
def extract_artwork_image_link_from_webpage(tree):
    link_text = lxml.html.tostring(LINK_CSS(tree)[0]).decode("utf-8")
    return LINK_REGEX.search(link_text).group(1)


@cop_out
def construct_new_filename_from_template_given(FN_TEMPLATE, artist,
                                               title, date):
    template = FN_TEMPLATE
    if "%a" in FN_TEMPLATE:
        template = template.replace("%a", artist)
    if "%t" in FN_TEMPLATE:
        template = template.replace("%t", title)
    if "%d" in FN_TEMPLATE:
        template = template.replace("%d", date)
    return template


@cop_out
def download_artwork_image(link):
    old_filename = wget.download(link)
    return old_filename


@cop_out
def create_subdirectories_to_place_artwork_image(path):
    os.makedirs(path, exist_ok=True)
    return True


@cop_out
def rename_downloaded_artwork_image(old_filename, FN_TEMPLATE, artist,
                                    title, date):
    tmp, extension = os.path.splitext(old_filename)
    new_filename = construct_new_filename_from_template_given(FN_TEMPLATE,
                                                              artist,
                                                              title,
                                                              date)
    has_path = SEP_DIRS.search(new_filename)
    if has_path:
        create_subdirectories_to_place_artwork_image(has_path.group(1))
    os.rename(old_filename, "{}{}".format(new_filename, extension))
    return True


def main():
    """doesn't do anything by itself that can fail"""
    THE_URL, FN_TEMPLATE = get_command_line_arguments()

    tree = parse_webpage(download_webpage(THE_URL))

    artist = extract_artist_name_from_webpage(tree)
    title, date = extract_title_and_date_from_webpage(tree)
    link = extract_artwork_image_link_from_webpage(tree)

    old_filename = download_artwork_image(link)
    rename_downloaded_artwork_image(old_filename, FN_TEMPLATE,
                                    artist, title, date)

    return True


if __name__ == '__main__':
    STATUS = main()
    sys.exit(STATUS)
