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

    @neovim.autocmd("VimEnter")
    def update(self):
        try:
            self.wid = self.api.workspaces()[0]["id"]
            self.projects = self.api.workspaces.projects(self.wid)
            self.tags = self.api.workspaces.tags(self.wid)
        except ConnectionError:
            self.echo("No network, disabled.")

    def echo(self, msg):
        self.nvim.command("echo '[Toggl.nvim] {}'".format(msg))

    @neovim.command("TogglEnable")
    def enable_toggl(self):
        self.echo("start watching")
        while True:
            try:
                cur = self.api.time_entries.current()["description"]
                self.nvim.vars["toggl_current"] = cur
            except ConnectionError:
                self.echo("Cannot access to Toggl API, disable toggl.nvim")
                break
            time.sleep(60)

    @neovim.command("TogglStart", range='', nargs="*")
    def start(self, args, range):
        projects = [arg[1:] for arg in args if arg[0] == "+"]
        if len(projects) > 1:
            raise RuntimeError("Multiple projects are specified.")
        if len(projects) == 1:
            name = projects[0]
        else:
            name = ""
        for p in self.projects:
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
        current = self.api.time_entries.current()
        if current is None:
            self.echo("No task is running.")
            return
        self.api.time_entries.stop(current["id"])
        self.echo("Task Stop: {}".format(current["description"]))
