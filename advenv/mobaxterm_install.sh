#!/bin/bash

HOME=/home/mobaxterm/

echo -n "Enter the home directory [$HOME]: "
read NEWHOME

[[ -n $NEWHOME ]] && HOME=$NEWHOME

echo "Using home directory $HOME"

cd ..
ln -s "$(pwd)/advenv" $HOME/.advenv
ln -s $HOME/.advenv/dotfiles/bashrc_moba $HOME/.load_advenv
ln -s $HOME/.advenv/dotfiles/vimrc7 $HOME/.vimrc
ln -s $HOME/.advenv/dotfiles/vim $HOME/.vim

cd
source $HOME/.load_advenv
