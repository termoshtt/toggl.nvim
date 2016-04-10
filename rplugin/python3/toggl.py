# -*- coding: utf-8 -*-

import neovim
import logging


@neovim.plugin
class Toggl(object):

    def __init__(self, nvim):
        self.nvim = nvim
        try:
            self.api_token = nvim.eval("g:toggl_api_token")
        except neovim.api.nvim.NvimError:
            logging.error("API Token cannot be read")

    @neovim.function("TogglAPIToken", sync=True)
    def get_api_token(self, args):
        return self.api_token
