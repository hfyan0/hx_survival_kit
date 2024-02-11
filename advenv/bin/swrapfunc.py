#!/usr/bin/env python3
import sys

def proc_wrapfunc(xs, init_indent):
    def is_closing_brac_far_away(xs):
        close_brac = [ xs.find(')'),
                       xs.find('>'),
                       xs.find('}'),
                       xs.find(']')]
        close_brac = filter(lambda x: x > 0, close_brac)
        return min(close_brac) > 8

    def proc_impl(
        xs,
        indent,
        outstr,
        curpos,
        lastx,prevwd):

        if not xs:
            return outstr

        x = xs[0]
        if x == ' ':
            newprevwd = ""
        else:
            newprevwd = prevwd+x

        if x == ' ' and lastx == ' ':
            newindent = indent
            newoutstr = outstr
            newcurpos = curpos
        elif x == '(' and len_to_closing_brac(xs) > 15:
            newindent = indent + 4
            newoutstr = outstr + x + '\n' + ' '*newindent
            newcurpos = indent
        elif x == ',' and is_closing_brac_far_away(xs[1:]):
            newindent = indent
            newoutstr = outstr + x + '\n' + ' '*indent
            newcurpos = indent
        elif x == '=':
            # if len(outstr) < 30:
            #     newindent = curpos + 2
            #     newoutstr = outstr + x
            #     newcurpos = curpos + 1
            # else:
            newindent = init_indent + 3
            newoutstr = outstr + x + '\n' + ' '*newindent
            newcurpos = newindent
        # elif x == ':' and outstr[-1:] == ':':
        #     newindent = curpos + 2
        #     newoutstr = outstr + x
        #     newcurpos = curpos + 1
        elif x == '{':
            newindent = curpos + 4
            newoutstr = outstr + x + '\n' + ' '*newindent
            newcurpos = newindent
        elif x == '}':
            newindent = indent - 4
            newoutstr = outstr + '\n' + ' '*newindent + x
            newcurpos = indent
        elif newprevwd == "return":
            newindent = curpos + 2
            newoutstr = outstr + x
            newcurpos = curpos + 1
        else:
            newindent = indent
            newoutstr = outstr + x
            newcurpos = curpos + 1

        return proc_impl(xs[1:],newindent,newoutstr,newcurpos,x,newprevwd)

    return ' '*init_indent + \
           proc_impl(
               xs,
               init_indent,
               "",
               init_indent,
               '',
               "")


def len_to_closing_brac(xs):
    def len_to_closing_brac_impl(xs,pos,no_of_open_brac):
        if not xs:
            return pos
        x = xs[0]
        if x == '(':
            return len_to_closing_brac_impl(
                        xs[1:],
                        pos+1,
                        no_of_open_brac+1)
        elif x == ')':
            if no_of_open_brac <= 1:
                return pos
            else:
                return len_to_closing_brac_impl(
                            xs[1:],
                            pos+1,
                            no_of_open_brac-1)
        else:
            return len_to_closing_brac_impl(
                        xs[1:],
                        pos+1,
                        no_of_open_brac)

    return len_to_closing_brac_impl(xs,0,0)


def preprocess(in_lines):
    init_indent = len(in_lines) - len(in_lines.lstrip())

    new_in_lines = in_lines \
                   .replace('\r', '') \
                   .replace('\n', '') \
                   .replace('=', " = ") \
                   .replace('(', " ( ") \
                   .replace(')', " ) ") \
                   .replace("    ", ' ') \
                   .replace("    ", ' ') \
                   .replace("   ", ' ') \
                   .replace("   ", ' ') \
                   .replace("  ", ' ') \
                   .replace("  ", ' ') \
                   .replace("  ", ' ') \
                   .replace("  ", ' ') \
                   .replace("  ", ' ') \
                   .replace("  ", ' ') \
                   .replace("{ ", '{') \
                   .replace(" (", '(') \
                   .replace("( ", '(') \
                   .replace(" )", ')') \
                   .replace(") ", ')') \
                   .replace(" ,", ',') \
                   .replace(", ", ',')
    new_in_lines = new_in_lines.strip()

    return init_indent,new_in_lines

###################################################
if __name__ == '__main__':

    init_indent,in_lines = preprocess(sys.stdin.read())

    print(proc_wrapfunc(in_lines, init_indent))
