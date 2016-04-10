toggl.nvim
===========
Toggl client in NeoVim using neovim/python-client

Usage
-----
Set your [API token](https://github.com/toggl/toggl_api_docs#api-token)

```vim
let g:toggl_api_token = "b51ff78xxxxxxxxxxxxxxxxxxxxxxxxx"
```

Start task

```vim
:TogglStart task name +project @tag1 @tag2
```

Stop current task

```vim
:TogglStop
```

License
--------
MIT License (see LICENSE file)
