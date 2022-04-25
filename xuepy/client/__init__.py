import os
import logging
import inspect
import requests
from typing import Dict, List, Any
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from xuepy.client import api
from xuepy.client.api.base import BaseAPI


def _is_api_endpoint(obj):
    return isinstance(obj, BaseAPI)


class Client:
    act = api.Interaction()

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(
        self,
        token: str,
        cookie: str,
        agent: str,
    ):

        requests.adapters.DEFAULT_RETRIES = 5
        self._session = requests.Session()
        heads = {
            "cookie": cookie,
            "User-Agent": agent,
            "Referer": "https://xue.cn",
            "Authorization": f"token {token}",
        }

        self._session.headers.update(heads)
        self._session.cookies["my_cookie"] = cookie
        self.baseurl = "https://xue.cn/hub/"

    def _request(self, method: str, url: str, relay: Dict = {}):
        resp = self._session.request(method=method, url=url, json=relay)

        print(resp.status_code, url, relay)
        if resp.status_code != 200:
            print(resp.text)
        return resp.json()

    def get(self, url: str, relay: Dict = {}):
        return self._request("get", url, relay)

    def post(self, url: str, relay: Dict = {}):
        return self._request("post", url, relay)
