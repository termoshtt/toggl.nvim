# -*- coding: utf-8 -*-

import neovim
import time
from .api import TogglAPI
from requests.exceptions import ConnectionError


@neovim.plugin
class Toggl(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.api_token = nvim.eval("g:toggl_api_token")
        self.api = TogglAPI(self.api_token)
        self.network_status = False

    def echo(self, msg):
        self.nvim.command("echo '[Toggl.nvim] {}'".format(msg))

    def entries(self):
        def convert(s):
            st = time.strftime("%FT%T%z", time.gmtime(s))
            return st[:-2] + ":" + st[-2:]

        now = time.time()
        return self.api.time_entries(
            convert(now-60*60*24*7),
            convert(now)
        )

    @neovim.command("TogglUpdate")
    def update(self):
        try:
            ws = self.api.workspaces
            self.wid = ws()[0]["id"]
            projects = ws.projects(self.wid)
            self.pmap = {p["id"]: p["name"] for p in projects}
            self.nvim.vars["toggl_projects"] = projects
            self.nvim.vars["toggl_tags"] = ws.tags(self.wid)
            self.nvim.vars["toggl_unite_task"] = [{
                "word": "{}\t[{}]\t({})".format(
                    t["description"], self.pmap[t["pid"]], t["duration"]),
                "source": "toggl/task",
                "kind": "toggl/task",
                "source__task": t
            } for t in self.entries()]
        except ConnectionError:
            self.echo("No network, disabled.")
        else:
            self.network_status = True

    @neovim.command("TogglEnable")
    def enable(self):
        self.update()
        while True:
            try:
                cur = self.api.time_entries.current()
                if cur and "description" in cur:
                    self.nvim.vars["toggl_current"] = cur["description"]
                else:
                    self.nvim.vars["toggl_current"] = "Don't forget time tracking!"
            except ConnectionError:
                self.echo("Cannot access to Toggl API, disable toggl.nvim")
                break
            time.sleep(15)

    @neovim.command("TogglStart", range='', nargs="*")
    def start(self, args, range):
        if not self.network_status:
            self.echo("toggl.nvim is not enabled.")
            return
        projects = [arg[1:] for arg in args if arg[0] == "+"]
        if len(projects) > 1:
            raise RuntimeError("Multiple projects are specified.")
        if len(projects) == 1:
            name = projects[0]
        else:
            name = ""
        for p in self.nvim.vars["toggl_projects"]:
            if p["name"] == name:
                pid = p["id"]
                break
        else:
            pid = 0

        tags = [arg[1:] for arg in args if arg[0] == "@"]
        desc = " ".join([arg for arg in args
                         if not arg.startswith(("+", "@"))])

        self.api.time_entries.start({
            "time_entry": {
                "description": desc,
                "pid": pid,
                "tags": tags,
                "created_with": "toggl.nvim",
            }
        })
        self.echo("Task Start: {}".format(desc))

    @neovim.command("TogglStop")
    def stop(self):
        if not self.network_status:
            self.echo("toggl.nvim is not enabled.")
            return
        current = self.api.time_entries.current()
        if current is None:
            self.echo("No task is running.")
            return
        self.api.time_entries.stop(current["id"])
        self.echo("Task Stop: {}".format(current["description"]))
