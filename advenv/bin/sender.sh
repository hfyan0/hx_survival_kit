#!/bin/bash

ymdhms=$(date +'%Y%m%d.%H%M%S')
tmpfolder="dat_${ymdhms}"
b64txt="dat_${ymdhms}.b64.txt"
file_list=file_list.txt

mkdir $tmpfolder

while read line; do
    cp -p ${line} ${tmpfolder}
done < $file_list

tar Jcf - ${tmpfolder} | base64 > ${b64txt}
rm -rf ${tmpfolder}
