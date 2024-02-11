#!/bin/bash
exec_print_result() {
    CMD=$1
    shift
    local width=60
    local cmd_desc="$@"
    local strlen=${#cmd_desc}
    echo -n "$cmd_desc"
    yes | $CMD > /dev/null 2>&1
    ret_code=$?
    for i in $(seq $(($width - $strlen))); do echo -n " "; done
    if [[ $ret_code -eq 0 ]]
    then
        local Color_Off="\033[0m"    # Text Reset
        local BGreen="\033[1;32m"    # Green
        echo -e "[${BGreen}  OK  ${Color_Off}]"
    else
        local Color_Off="\033[0m"    # Text Reset
        local BRed="\033[1;31m"      # Red
        echo -e "[${BRed}FAILED${Color_Off}]"
    fi
    return $ret_code
}

# date
# exec_print_result "touch /tmp/wewewerewr" "Doing a job that should be OK."
# exec_print_result "rm /root/asdflwwerwerwer qwekqwetqssd" "Doing a job that should fail."
