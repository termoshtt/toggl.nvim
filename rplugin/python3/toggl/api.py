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

    def _put(self, rest):
        url = op.join(self.base_url, rest)
        r = requests.put(url, auth=(self.api_token, "api_token"))
        return r.json()

    def _post(self, rest, data):
        url = op.join(self.base_url, rest)
        r = requests.post(
            url, data=json.dumps(data),
            auth=(self.api_token, "api_token")
        )
        return r.json()


class Workspaces(API_base):
    def __call__(self):
        return self._get("workspaces")

    def projects(self, wid):
        return self._get("workspaces/{}/projects".format(wid))

    def tags(self, wid):
        return self._get("workspaces/{}/tags".format(wid))


class TimeEntries(API_base):
    def __call__(self, start, end):
        return self._get("time_entries", start_date=start, end_date=end)

    def start(self, data):
        return self._post("time_entries/start", data=data)["data"]

    def stop(self, entry_id):
        return self._put("time_entries/{}/stop".format(entry_id))["data"]

    def current(self):
        r = self._get("time_entries/current")
        if "data" in r:
            return r["data"]
        return None


class TogglAPI(object):
    def __init__(self, api_token):
        self.workspaces = Workspaces(api_token)
        self.time_entries = TimeEntries(api_token)
