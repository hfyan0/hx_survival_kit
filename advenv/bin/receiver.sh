#!/bin/bash

tmpfile=$(mktemp)
vim $tmpfile

cat $tmpfile | ./encrypt.py d | base64 --decode | tar Jxf -
rm -f $tmpfile
