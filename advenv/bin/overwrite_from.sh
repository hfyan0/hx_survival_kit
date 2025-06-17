#!/bin/bash

if [[ $# -ne 2 ]]
then
    echo "usage: $0 [xxx_md5.xz.b64.txt] [xxx_md5.txt]"
    exit
fi

compressed_file=$1
target_file=$2

cat $compressed_file | base64 --decode | unxz > $target_file
