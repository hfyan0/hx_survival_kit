#!/bin/bash

if [[ -z $HOME ]]
then
    HOME=/home/$(whoami)/
fi

cd ..
mv advenv $HOME/.advenv
ln -s $HOME/.advenv/dotfiles/bashrc $HOME/.load_advenv
ln -s $HOME/.advenv/local/nvim-linux64_0.9.4/bin/nvim $HOME/.advenv/bin/nvim
ln -s $HOME/.advenv/dotfiles/vimrc $HOME/.vimrc
[[ ! -d $HOME/.config ]] && mkdir $HOME/.config
ln -s $HOME/.advenv/dotfiles/vim $HOME/.config/nvim
ln -s $HOME/.advenv/dotfiles/vim $HOME/.vim
ln -s $HOME/.advenv/dotfiles/tigrc $HOME/.tigrc
ln -s $HOME/.advenv/dotfiles/tmux.conf $HOME/.tmux.conf
ln -s $HOME/.advenv/dotfiles/gitconfig $HOME/.gitconfig
ln -s $HOME/.advenv/dotfiles/ctagsrc $HOME/.ctagsrc
ln -s $HOME/.advenv/local/git_2.30.2/bin/git $HOME/.advenv/bin/git
ln -s $HOME/.advenv/local/pandoc-3.1.11.1/bin/pandoc $HOME/.advenv/bin/pandoc
ln -s $HOME/.advenv/bin/fromdos $HOME/.advenv/bin/todoes
ln -s $HOME/.advenv/bin/ncat $HOME/.advenv/bin/nc

cd
source $HOME/.load_advenv

echo "Download git from: https://github.com/git/git/releases/tag/v2.30.2"
