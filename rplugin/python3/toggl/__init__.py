# -*- coding: utf-8 -*-

import neovim
from .api import TogglAPI


@neovim.plugin
class Toggl(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.api_token = nvim.eval("g:toggl_api_token")
        self.api = TogglAPI(self.api_token)
        self.update()

    @neovim.function("TogglUpdate", sync=True)
    def update(self):
        self.wid = self.api.workspaces()[0]["id"]
        self.projects = self.get_projects([])

    def echo(self, msg):
        self.nvim.command("echo '{}'".format(msg))

    @neovim.function("TogglAPIToken", sync=True)
    def api_token(self, args):
        return self.api_token

    @neovim.function("TogglGetCurrent", sync=True)
    def get_current(self, args):
        return self.api.time_entries.current()

    @neovim.function("TogglGetProjects", sync=True)
    def get_projects(self, args):
        return self.api.workspaces.projects(self.wid)

    @neovim.function("TogglGetTags", sync=True)
    def get_tags(self, args):
        return self.api.workspaces.tags(self.wid)

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
