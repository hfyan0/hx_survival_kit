#!/bin/bash

tmpfile=$(mktemp)

if [[ $# -eq 0 ]]
then
    vim $tmpfile
else
    cat $1 > $tmpfile
fi

cat $tmpfile | ./encrypt.py d | base64 --decode | tar Jxf -

rm -f $tmpfile
