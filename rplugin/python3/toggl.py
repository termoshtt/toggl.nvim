# -*- coding: utf-8 -*-

import neovim


@neovim.plugin
class Toggl(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.api_token = nvim.eval("g:toggl_api_token")

    @neovim.function("TogglAPIToken", sync=True)
    def get_api_token(self, args):
        return self.api_token
