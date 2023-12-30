#!/usr/bin/env python3
import sys

def get_variable(xs):
    def get_variable_impl(xs,varb):
        if not xs:
            return varb
        x = xs[0]
        if x == '=':
            return varb
        elif ';' in x:
            return x.replace(';','')
        else:
            return get_variable_impl(xs[1:],x)

    return get_variable_impl(xs,"")

def align_anchors(in_lines,anchor_locs):
    def align_line(line, align_loc, anchor_loc):
        return line[:anchor_loc-1] + " " + ' '*(align_loc-anchor_loc) + line[anchor_loc:]
    max_anchor_loc = max(anchor_locs)
    return [align_line(line,max_anchor_loc,type_end) for line,type_end in zip(in_lines,anchor_locs)]

def decorate_eol(line,comment):
    ret_line = line.rstrip()
    if not ret_line:
        return ret_line
    else:
        if ret_line[-1] == ',':
            need_semi_colon = False
        elif ret_line[-1] == ')' and ret_line.find('(') < 0:
            need_semi_colon = False
        else:
            need_semi_colon = True

        return ret_line + \
               (';' if need_semi_colon else '') + \
               (' '+comment if comment else '')

def get_comment(line):
    c = line.find("//")
    if c < 0:
        return ""
    else:
        return line[c:]

def rm_comment(line):
    c = line.find("//")
    if c < 0:
        return line
    else:
        return line[:c]

def find_whole_word(line,s):
    x = line.find(' ' + s + ' ')
    if x >= 0:
        return x + 1

    y = ' ' + s
    if line[-(len(y)):] == y:
        return len(line)-len(s)

    y = s + ' '
    if line[:(len(y))] == y:
        return 0

def align_type(sinput):
    in_lines = [line.replace('\n','').replace(';','').replace('='," = ") for line in sinput]
    if len(in_lines) > 0 and not in_lines[0].strip():
        in_lines = sinput.split('\n')

    comments = [get_comment(line) for line in in_lines]
    in_lines = [rm_comment(line)  for line in in_lines]

    in_matrix = [line.strip().replace(';','').split() for line in in_lines]

    variables = [get_variable(line) for line in in_matrix]

    type_aligned_lines = align_anchors(
                             in_lines,
                             [find_whole_word(line,varb) for line,varb in zip(in_lines,variables)])
    type_eq_aligned_lines = align_anchors(
                                type_aligned_lines,
                                [(len(line)+1 if line.find('=') < 0 else line.find('='))
                                    for line in type_aligned_lines])

    type_eq_aligned_lines = [decorate_eol(x,comment) for x,comment in zip(type_eq_aligned_lines,comments)]

    print('\n'.join(type_eq_aligned_lines))

###################################################

if __name__ == "__main__":
    align_type(sys.stdin)
