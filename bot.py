#!/usr/bin/env python
from pathlib import Path
from subprocess import Popen
from urllib.parse import urlparse, urlunparse, urljoin, quote
import io
import os
import random
import sys
import traceback

from pyquery import PyQuery as pq
from twython import Twython
import requests

MAX_PAGE_TRY = 200
RANDOM_PAGE_URL = 'https://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA'

def is_content_element(element):
    return not (
           pq(element).parents('div.metadata')
        or pq(element).parents('.noprint')
        or pq(element).parents('.thumbcaption')
    )


def full_image_url(img_element):
    href = pq(img_element).parents('a').attr('href')
    image_page_url = urljoin('https://ja.wikipedia.org', href)

    src = pq(url=image_page_url)('#file img').attr('src')
    p = urlparse(src)
    return urlunparse(('http',) + p[1:6])


class BadWikipediaPageError(ValueError):
    pass

def post_random_page_image():
    twitter = Twython(
        os.environ['TWITTER_BOT_APP_KEY'],
        os.environ['TWITTER_BOT_APP_SECRET'],
        os.environ['TWITTER_BOT_OAUTH_TOKEN'],
        os.environ['TWITTER_BOT_OAUTH_TOKEN_SECRET'],
    )

    d = pq(url=RANDOM_PAGE_URL)
    title = d('title').text().split('-')[0].strip()
    if not title:
        raise BadWikipediaPageError("Title is empty")

    elements = d('li.gallerybox img, .thumb img')
    elements = [x for x in elements if is_content_element(x)]

    if not elements:
        raise BadWikipediaPageError("No images", title)

    img = random.choice(elements)
    text = pq(pq(img).parents('.gallerybox, .thumb')).text()

    if not text:
        raise BadWikipediaPageError("Text is empty", title)

    r = requests.get(full_image_url(img))

    status = "「{}」の項「{}」\nhttp://ja.wikipedia.org/wiki/{}".format(title, text, quote(title))
    if len(status) > 140:
        exceed = len(status) - 140
        if len(text) - exceed < 5:
            raise BadWikipediaPageError('text is too long ({}, {})'.format(repr(title), repr(text)))
        else:
            text = text[: -(exceed + 1)] + '…'
        status = "「{}」の項「{}」\nhttp://ja.wikipedia.org/wiki/{}".format(title, text, quote(title))

    twitter.update_status_with_media(status=status, media=io.BytesIO(r.content))
    print("Posted", repr(status))



def main():
    for _ in range(MAX_PAGE_TRY):
        try:
            r = post_random_page_image()
        except Exception as e:
            traceback.print_exc()
        else:
            sys.exit(0)
    else:
        sys.exit(1)



if __name__ == '__main__':
    main()
