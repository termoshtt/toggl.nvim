" FILE: unite/kinds/task.vim
" AUTHOR: Toshiki Teramura <toshiki.teramura@gmail.com>
" LICENCE: MIT

let s:save_cpo = &cpo
set cpo&vim

let s:kind_task = {
      \ 'name' : 'toggl/task',
      \ 'action_table' : {},
      \ 'default_action' : 'restart',
      \}

let s:kind_task.action_table.restart = {
      \ 'description': "restart selected task"
      \ }

function! s:kind_task.action_table.restart.func(candidate) abort
  call TogglRestart(a:candidate.source__task)
endfunction

function! unite#kinds#toggl#define() abort
  return [s:kind_task]
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
