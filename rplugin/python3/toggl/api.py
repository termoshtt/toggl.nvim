# -*- coding: utf-8 -*-

import os.path as op
import json
import requests


class API_base(object):

    base_url = "https://www.toggl.com/api/v8/"

    def __init__(self, api_token):
        self.api_token = api_token

    def _get(self, rest, **params):
        url = op.join(self.base_url, rest)
        r = requests.get(
            url, params=params,
            auth=(self.api_token, "api_token")
        )
        return r.json()

    def _post(self, rest, data):
        url = op.join(self.base_url, rest)
        r = requests.post(
            url, data=json.dumps(data),
            auth=(self.api_token, "api_token")
        )
        return r.json()


class Workspaces(API_base):
    def get(self):
        return self._get("workspaces")

    def projects(self, wid):
        return self._get("workspaces/{}/projects".format(wid))

    def tags(self, wid):
        return self._get("workspaces/{}/tags".format(wid))


class TimeEntries(API_base):
    def current(self):
        return self._get("time_entries/current")


class TogglAPI(object):
    def __init__(self, api_token):
        self.workspaces = Workspaces(api_token)
        self.time_entries = TimeEntries(api_token)
