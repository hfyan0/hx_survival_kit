#!/bin/bash

b64_root=base64.root.txt
tmpfile1=$(mktemp)
tmpfile2=$(mktemp)

user_input=$1
if [[ -z $user_input ]]
then
    user_input=3
fi

cat ${b64_root} > $tmpfile1

for p in $(seq $user_input)
do
    cat $tmpfile1 | shuf > $tmpfile2
    cat $tmpfile2 > $tmpfile1
done

paste base64.root.txt $tmpfile1 | tr '\t' ','

rm -f $tmpfile1 $tmpfile2
