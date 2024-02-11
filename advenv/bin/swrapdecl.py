#!/usr/bin/env python3
from swrapfunc import *
from saligntype import align_type

def find_second_eol(s):
    def find_second_eol_impl(s,loc,eol_num):
        if eol_num == 2:
            return loc+1
        else:
            i = s.find('\n')
            return find_second_eol_impl(
                       s[i+1:],
                       loc+i,
                       eol_num+1)
    return find_second_eol_impl(s,0,0)

if __name__ == '__main__':

    init_indent,in_lines = preprocess(sys.stdin.read())

    output = proc_wrapfunc(in_lines, init_indent)

    new_output = ' '*init_indent + output[init_indent:].replace(' ','\n',1)

    loc = find_second_eol(new_output)

    rettype_funname = new_output[:loc]
    arg_type_name   = new_output[(loc+1):]

    print(rettype_funname)
    try:
        align_type(arg_type_name)
    except Exception as e:
        print(arg_type_name)
