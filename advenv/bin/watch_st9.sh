#!/bin/bash
filepath=$(st n 9)

get_last_mod_time()
{
    stat $filepath | grep Modify
}

last_output=$(get_last_mod_time)
while [ 1 ]
do
    this_output=$(get_last_mod_time)
    if [[ $this_output != $last_output ]]
    then
        clear
        cat $filepath
        last_output=$this_output
    else
        sleep 0.2
    fi
done
