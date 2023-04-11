#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import os
import json
import requests
import fc2
from Crypto.Cipher import AES
from flask import Flask, request, make_response, jsonify


def async_proxy(event):
    FEISHU_CHATGPT_BASE_URL = os.environ.get('FEISHU_CHATGPT_BASE_URL', '')
    ALIYUN_FC_ENDPOINT = os.environ.get('ALIYUN_FC_ENDPOINT', '')
    ALIYUN_FC_ASYNC_TASK_SERVICE_NAME = os.environ.get(
        'ALIYUN_FC_ASYNC_TASK_SERVICE_NAME', '')
    ALIYUN_FC_ASYNC_TASK_FUNCTION_NAME = os.environ.get(
        'ALIYUN_FC_ASYNC_TASK_FUNCTION_NAME', 'async_task')
    ALIYUN_ACCESS_KEY_ID = os.environ.get('ALIYUN_ACCESS_KEY_ID', '')
    ALIYUN_ACCESS_KEY_SECRET = os.environ.get(
        'ALIYUN_ACCESS_KEY_SECRET', '')
    url = FEISHU_CHATGPT_BASE_URL + '/webhook/' + event
    lark_headers = {
        'X-Lark-Signature': request.headers.get('X-Lark-Signature', ''),
        'X-Lark-Request-Timestamp': request.headers.get('X-Lark-Request-Timestamp', ''),
        'X-Lark-Request-Nonce': request.headers.get('X-Lark-Request-Nonce', '')
    }
    client = fc2.Client(
        endpoint=ALIYUN_FC_ENDPOINT,
        accessKeyID=ALIYUN_ACCESS_KEY_ID,
        accessKeySecret=ALIYUN_ACCESS_KEY_SECRET)
    payload = {
        'url': url,
        'method': 'POST',
        'headers': lark_headers,
        'data': request.get_data().decode("utf-8")
    }
    payload = json.dumps(payload)
    headers = {
        'x-fc-invocation-type': 'Async'
    }
    client.invoke_function(ALIYUN_FC_ASYNC_TASK_SERVICE_NAME,
                           ALIYUN_FC_ASYNC_TASK_FUNCTION_NAME, headers=headers, payload=payload)


app = Flask(__name__)


@app.route("/webhook/event", methods=['GET', 'POST'])
def feishu_webhook_event():
    default_resp = make_response(jsonify({}))
    payload = request.get_json()
    if payload.get('encrypt', None):
        encrypt = payload['encrypt']
        FEISHU_ENCRYPT_KEY = os.environ.get('FEISHU_ENCRYPT_KEY', '')
        cipher = AESCipher(FEISHU_ENCRYPT_KEY)
        decrypt = cipher.decrypt_string(encrypt)
        payload: dict = json.loads(decrypt)
    if payload.get('type', None) == 'url_verification':
        FEISHU_CHATGPT_BASE_URL = os.environ.get('FEISHU_CHATGPT_BASE_URL', '')
        url = FEISHU_CHATGPT_BASE_URL + '/webhook/event'
        headers = {
            'X-Lark-Signature': request.headers.get('X-Lark-Signature', ''),
            'X-Lark-Request-Timestamp': request.headers.get('X-Lark-Request-Timestamp', ''),
            'X-Lark-Request-Nonce': request.headers.get('X-Lark-Request-Nonce', '')
        }
        r = requests.post(url, headers=headers, data=request.get_data())
        return make_response(jsonify(r.json()))

    async_proxy('event')
    return default_resp


@app.route("/webhook/card", methods=['GET', 'POST'])
def feishu_webhook_card():
    default_resp = make_response(jsonify({}))
    payload: dict = request.get_json()
    if payload.get('type', None) == 'url_verification':
        ret = {
            'challenge': payload['challenge']
        }
        resp = make_response(jsonify(ret))
        return resp
    async_proxy('card')
    return default_resp


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')


def main():
    app.run(host='0.0.0.0', port=9000)


if __name__ == '__main__':
    main()
