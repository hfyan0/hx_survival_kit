#!/bin/bash

ymdhms=$(date +'%Y%m%d.%H%M%S')
tmpfolder="dat_${ymdhms}"
b64txt="dat_${ymdhms}.b64.txt"
file_list=file_list.txt

mkdir $tmpfolder

while read line; do
    if [[ -n ${line} ]]
    then
        cp -p "${line}" ${tmpfolder}
    fi
done < $file_list

tar Jcf - ${tmpfolder} | base64 | ./encrypt.py e > ${b64txt}
rm -rf ${tmpfolder}
echo ${b64txt}
