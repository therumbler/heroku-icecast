#!/usr/bin/env python3

import json
import logging
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

HEROKU_TOKEN = os.environ['HEROKU_TOKEN']

logger = logging.getLogger(__name__)

def call(endpoint, data=None, method="GET"):
    url = f"https://api.heroku.com/{endpoint}"
    headers = {
        'Authorization': f"Bearer {HEROKU_TOKEN}",
        'Accept': "application/vnd.heroku+json; version=3",
        'Content-Type': 'application/json',
    }
    data_string = None
    if data:
        data_string = json.dumps(data).encode()
        method = "POST"

    req = Request(url, data=data_string)
    req.method = method.upper()

    for k, v in headers.items():
        req.add_header(k, v)

    logger.info('loading %s ... with token %s', url, HEROKU_TOKEN)
    try:
        resp = urlopen(req)
        logger.info('got resp')
    except HTTPError as ex:
        logger.error('HTTPError %s', ex.code)
        resp = ex

    data = json.load(resp)
    return data

def get_apps():
    return call('apps', method='GET')


def create_app(name):
    return call('apps', method='POST', data={'name': name})

def delete_app(app_id):
    return call(f"apps/{app_id}", method="DELETE")


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    apps = get_apps()
    for app in apps:
        print(app['id'], app['name'])

if __name__ == '__main__':
    main()

