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
        # method = "POST"

    req = Request(url, data=data_string)
    req.method = method.upper()

    for k, v in headers.items():
        req.add_header(k, v)

    logger.info('%s %s data=%r ', req.method, url, data)
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

def release_app(app_id, docker_image_id):    
    data = {
        "updates": [
            {
                "type": "server",
                "docker_image": docker_image_id,
            }
        ]
    }
    return call(f"apps/{app_id}/formation", method="PATCH", data=data)

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    apps = get_apps()
    for app in apps:
        print(app['id'], app['name'])

    app_name = "beats-with-benji-icecast"
    # app = create_app(name=app_name)
    # print(app)

    docker_image_id = "23f35c9afecec554719cbc950e0bc08229167e8e7ac812ce82c4aca2923d3793"
    app_id = "effcfd30-9553-4a4d-9925-3a22e60c4f0c"
    release_app(app_id=app_id, docker_image_id=docker_image_id)
if __name__ == '__main__':
    main()
