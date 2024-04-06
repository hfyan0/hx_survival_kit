#!/bin/bash

if [[ $# -eq 0 ]]
then
    echo "Usage: $(basename $0) [base64 file]"
    exit
fi

cat $1 | base64 --decode | tar Jxf -
