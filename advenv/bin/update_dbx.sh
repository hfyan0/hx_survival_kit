#!/bin/bash

if [[ $# -eq 0 ]]
then
    echo "Usage: $(basename $0) [extracted folder]"
    exit
fi

folder=$1
for f in $folder/*
do
    echo $f
    vimdiff $f $(cat file_list.txt | grep $(basename $f))
done
