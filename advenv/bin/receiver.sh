#!/bin/bash

tmpfile=$(mktemp)
tmpfile2=$(mktemp).gpg

if [[ $# -eq 0 ]]
then
    vim $tmpfile
else
    cat $1 > $tmpfile
fi

if [[ -z $(cat $tmpfile) ]]
then
    echo "Missing data. Exiting..."
    exit
fi

cat $tmpfile | tr -d '\r' | ./encrypt.py d | base64 --decode > $tmpfile2
# gpg --ignore-mdc-error -d $tmpfile2 | tar Jxf -
gpg --ignore-mdc-error -d $tmpfile2 | unxz | tar xf -

rm -f $tmpfile $tmpfile2
