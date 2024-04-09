#!/bin/bash

tmpfile=$(mktemp)
vim $tmpfile

cat $tmpfile | ./encrypt_b64.py d | base64 --decode | tar Jxf -
rm -f $tmpfile
