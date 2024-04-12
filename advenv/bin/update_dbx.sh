#!/bin/bash

if [[ $# -eq 0 ]]
then
    echo "Usage: $(basename $0) [extracted folder]"
    exit
fi

folder=$1
for f in $folder/*
do
    file1=$f
    file2=$(cat file_list.txt | grep $(basename $f))
    echo
    echo "=============================="
    md5sum $file1 $file2
    echo
    vimdiff $file1 $file2

    if [[ $(md5sum $file1 | awk '{print $1}') != $(md5sum $file2 | awk '{print $1}') ]]
    then
        echo "Overwrite with $file1 ? [yes|N]"
        read user_input
        if [[ $user_input == "yes" || $user_input == "YES" ]]
        then
            cat $file1 > $file2
            echo "$file2 was overwritten"
            md5sum $file1 $file2
            echo "Press Enter to continue..."
            read
        fi
    fi
done
