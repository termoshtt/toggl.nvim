# -*- coding: utf-8 -*-

import neovim
from .api import TogglAPI


@neovim.plugin
class Toggl(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.api_token = nvim.eval("g:toggl_api_token")
        self.api = TogglAPI(self.api_token)
        self.wid = self.api.workspaces.get()[0]["id"]

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
