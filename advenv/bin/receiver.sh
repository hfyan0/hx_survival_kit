#!/bin/bash

tmpfile=$(mktemp)
vim $tmpfile

cat $tmpfile | base64 --decode | tar Jxf -
rm -f $tmpfile
