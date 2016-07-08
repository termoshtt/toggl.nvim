" FILE: unite/sources/toggl.vim
" AUTHOR:  Toshiki TERAMUREA <toshiki.teramura@gmail.com>
" License: MIT

let s:save_cpo = &cpo
set cpo&vim

let s:src_task = {
      \ 'name': 'toggl/task'
      \ }

function! s:src_task.gather_candidates(args,context) abort
  return exists("g:toggl_unite_task") ? reverse(g:toggl_unite_task): []
endfunction

function! unite#sources#toggl#define() 
  return [s:src_task]
endfunction 

let &cpo = s:save_cpo
unlet s:save_cpo

