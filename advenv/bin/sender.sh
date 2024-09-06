#!/bin/bash

ymdhms=$(date +'%Y%m%d.%H%M%S')
tmpfolder="dat_${ymdhms}"
b64txt="dat_${ymdhms}.b64.txt"
file_list=file_list.txt
tmpfile=$(mktemp)

mkdir $tmpfolder

while read line; do
    if [[ -n ${line} ]]
    then
        cp -p "${line}" ${tmpfolder}
    fi
done < $file_list

# tar Jcf ${tmpfile} ${tmpfolder}
tar cf - ${tmpfolder} | xz -9 > ${tmpfile}
ps ux | grep gpg-agent | awk "{print \$2}" | tr "\n" "\0" | xargs -0 kill
gpg -c $tmpfile

cat ${tmpfile}.gpg | base64 | ./encrypt.py e > ${b64txt}
rm -rf ${tmpfolder}
echo "--------------------------------------------------"
ls -lh ${b64txt}
echo "--------------------------------------------------"


rm -f $tmpfile
