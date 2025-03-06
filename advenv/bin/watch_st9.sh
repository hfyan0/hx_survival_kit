#!/bin/bash
filepath=$(st n 9)

get_last_mod_time()
{
    stat $filepath | grep Modify
}

last_output=$(get_last_mod_time)
while [ 1 ]
do
    if [[ $(get_last_mod_time) != $last_output ]]
    then
        echo "Oh"
        last_output=$(get_last_mod_time)
    else
        sleep 0.2
    fi
done
