#!/bin/bash

if [[ -z $HOME ]]
then
    HOME=/home/$(whoami)/
fi

unlink $HOME/.load_advenv
unlink $HOME/.vimrc
unlink $HOME/.config/nvim
unlink $HOME/.vim
unlink $HOME/.tigrc
unlink $HOME/.tmux.conf
unlink $HOME/.gitconfig

rm -rf $HOME/.advenv
