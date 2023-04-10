#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests


def handler(event, context):
    req = json.loads(event)
    headers = req.get('headers', None)
    params = req.get('params', None)
    data = req.get('data', None)
    if data:
        data = data.encode('utf-8')
    json_data = req.get('json', None)
    requests.request(req['method'], req['url'], params=params,
                     json=json_data, data=data, headers=headers)
    return {}
