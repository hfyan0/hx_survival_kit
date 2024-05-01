#!/usr/bin/env python3
import sys, os
import curses
import curses.ascii
from datetime import datetime
from collections import namedtuple

State = namedtuple('State', 'text pos')

def expand_last_word(s,abbrev_dict):
    risa = reversed([(c.isalpha() or c.isdigit()) for c in s])
    risnota = [i for i,a in enumerate(risa) if not a]

    if not risnota:
        return abbrev_dict.get(s,s)
    else:
        loc = len(s) - risnota[0] - 1
        w = s[(loc+1):]
        ab = abbrev_dict.get(w,w)
        return s[:(loc+1)] + ab

def clean_str(s):
    s = s.strip()
    for i in range(10):
        s = s.replace('  ',' ')
        s = s.replace(' @@','@@')
        s = s.replace('@@ ','@@')
    return s


def toggle_case(c):
    if c == c.upper():
        return c.lower()
    elif c == c.lower():
        return c.upper()
    else:
        return c


def toggle_sentence_case(s, to_upper_case):
    delim_list = ["@@", ". ", "- ", "> ", "? ", "! "]
    first_delim_list = [x[0] for x in delim_list]

    def change_sentence_case_impl(s_remain, prev_match, s_out):
        if not s_remain:
            return s_out
        else:
            c = s_remain[0]
            ns_remain = s_remain[1:]

            print(prev_match, c)

            if prev_match in delim_list:
                if (prev_match[-1] + c) in delim_list:
                    return change_sentence_case_impl(
                               ns_remain,
                               prev_match[-1] + c,
                               s_out + c)
                else:
                    return change_sentence_case_impl(
                               ns_remain,
                               "",
                               # s_out + toggle_case(c))
                               s_out + (c.upper() if to_upper_case else c.lower()))
            elif len(prev_match) == 1:
                if (prev_match + c) in delim_list:
                    return change_sentence_case_impl(
                               ns_remain,
                               (prev_match + c),
                               s_out + c)
                elif c in first_delim_list:
                    return change_sentence_case_impl(
                               ns_remain,
                               c,
                               s_out + c)
                else:
                    return change_sentence_case_impl(
                               ns_remain,
                               "",
                               s_out + c)
            else:
                if c in first_delim_list:
                    return change_sentence_case_impl(
                               ns_remain,
                               c,
                               s_out + c)
                else:
                    return change_sentence_case_impl(
                               ns_remain,
                               "",
                               s_out + c)

    return change_sentence_case_impl(s, "", "")


def update_state(state,k,width,height,abbrev_dict):
    max_len = width*(height-2)

    s,pos = state

    if k is None:
        ns = s
        npos = pos
    elif k == 1: # C-a
        ns = s
        npos = 0
    elif k == 5: # C-e
        ns = s
        npos = len(s)
    elif k == 11: # C-k
        ns = s[:pos]
        npos = pos
    elif k == 14: # C-n
        loc = s[:pos].rfind(' ', 0, pos-1)
        cur_prefix = s[:pos].strip() \
                     if loc < 0 \
                     else s[loc:pos].strip()
        if not cur_prefix:
            ns = s
            npos = pos
        else:
            words = [ (x[:len(cur_prefix)].strip(),
                       x[len(cur_prefix):].strip())
                       for x in s.split(' ') ]
            ns = s
            npos = pos
            for prefix,suffix in words:
                if prefix == cur_prefix:
                    ns = s[:pos] + suffix + s[pos:]
                    npos = pos + len(suffix)
                    break
    elif k == 21: # C-u
        ns = s[pos:]
        npos = 0
    elif k == 23: # C-w
        loc = s.rfind(' ', 0, pos-1)
        if loc < 0:
            ns = s[pos:]
            npos = 0
        else:
            ns = s[:loc] + ' ' + s[pos:]
            npos = len(s[:loc]) + 1
    elif k in [32, 64]: # space / @
        if pos == 0 or (k == 32 and s[pos-1] == ' '):
            # repeated spacesstay where you are
            ns = s
            npos = pos
        else:
            # expand word
            es = expand_last_word(s[:pos],abbrev_dict)
            ns = es + chr(k) + s[pos:]
            npos = len(es)+1
    elif k == 126: # home / end
        ns = s
        npos = pos
    elif k in [33,
               63,
               44,
               46,
               45,
               61,
               91,
               93,
               40,
               41,
               123,
               125,
               47,
               124,
               92,
               34,
               39,
               58,
               59,
               10,
               27,
               9]:
        # ! ? , . - = [ ] ( ) { } / | \ " ' : ; enter esc tab
        # expand word
        es = expand_last_word(s[:pos],abbrev_dict)
        ns = es + chr(k) + s[pos:]
        npos = len(es)+1
    elif k in [258,259]: # up down
        ns = s
        npos = pos
    elif k == 260: # left
        if pos > 0 and pos < len(s) and s[pos] == ' ' and s[pos-1] == ' ':
            ns = s[:pos] + s[(pos+1):]
            npos = pos
        else:
            ns = s
            npos = max(pos-1,0)
    elif k == 261: # right
        if pos > 0 and pos < len(s) and s[pos] == ' ' and s[pos-1] == ' ':
            ns = s[:pos] + s[(pos+1):]
            npos = pos
        else:
            ns = s
            npos = min(pos+1,len(s))
    elif k in [8,127,263]: # backspace, C-h
        if pos >= 1:
            ns = s[:(pos-1)] + s[pos:]
            npos = pos - 1
        else:
            ns = s
            npos = pos
    elif k in [4,330]: # delete C-d
        ns = ''.join([c for i,c in enumerate(s) if i != pos])
        npos = pos
    elif k == "alt-b":
        ns = s
        stop_cs = [' ','(','[','{','@']
        locs = [s.rfind(c, 0, max(pos-1,0)) for c in stop_cs]
        loc = max(max(locs),0)
        if s[loc] in stop_cs:
            npos = min(loc+1,len(s))
        else:
            npos = loc
    elif k == "alt-c":
        # toggle sentence case
        if not s:
            ns = s
            npos = pos
        else:
            to_upper_case = (s[0] == s[0].lower())
            ns = toggle_case(s[0]) + s[1:]
            ns = toggle_sentence_case(ns, to_upper_case)
            npos = pos
    elif k == "alt-f":
        ns = s
        loc1 = s.find(' ', pos+1)
        loc2 = s.find('@', pos+1)

        if loc1 * loc2 > 0:
            loc = min(loc1, loc2)
        else:
            loc = max(loc1, loc2)

        if loc < 0:
            npos = len(s)
        else:
            npos = loc
    elif k == "alt-d":
        start_pos = (pos+1) if s[pos] in [' ','@'] else pos
        loc1 = s.find(' ',start_pos)
        loc2 = s.find('@',start_pos)

        if loc1 * loc2 > 0:
            loc = min(loc1, loc2)
        else:
            loc = max(loc1, loc2)

        if loc < 0:
            ns = s[:pos]
            npos = len(ns)
        else:
            ns = s[:pos] + s[loc:]
            npos = len(s[:pos])
    else:
        ns = s[:pos] + chr(k) + s[pos:]
        npos = pos + 1

    ns = ns.replace('\n','')[:max_len]
    npos = max(min(npos,max_len),0)

    return State(ns,npos)

def get_cursor_xy(pos,width):
    cursor_x = pos % width
    cursor_y = pos // width
    return cursor_x,cursor_y

def draw_menu(stdscr):

    if outfile:
        with open(outfile, "r") as f:
            prev_s = '@@'.join([line.strip() for line in f])
            state = State(prev_s,len(prev_s))
    else:
        state = State("",0)

    with open("~/.advenv/dotfiles/abbrev",'r') as f:
        lines = [ line.strip() for line in f]
        abbrev_dict = dict([ (line.split(' ')[1],' '.join(line.split(' ')[2:])) for line in lines])

    dt  = datetime.now().strftime("%Y-%m-%d")
    dtm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    abbrev_dict["ymd"] = dt
    abbrev_dict["Ymd"] = dt
    abbrev_dict["YMD"] = dt
    abbrev_dict["yh"] = dtm
    abbrev_dict["YH"] = dtm
    abbrev_dict["192"] = "192.168.31."
    abbrev_dict["127"] = "127.0.0.1"

    k = 0

    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    while True:
        if k in [10,27]: # enter / escape
            state = update_state(state,k,width,height,abbrev_dict)
            break

        ###################################################
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        ###################################################
        # status bar
        sStatusBar = "Press <Enter> to exit | {} |".format(k)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, sStatusBar)
        stdscr.addstr(height-1, len(sStatusBar), " " * (width - len(sStatusBar) - 1))
        stdscr.attroff(curses.color_pair(3))

        ###################################################
        stdscr.addstr(0, 0, state.text)
        cursor_x,cursor_y = get_cursor_xy(state.pos,width)
        stdscr.move(cursor_y, cursor_x)

        ###################################################
        stdscr.refresh()
        k = stdscr.getch()

        if k == 27: # ALT
            stdscr.nodelay(True)
            ch = stdscr.getch() # get the key pressed after ALT
            if ch == -1:
                pass
            elif ch == 98:
                k = "alt-b"
            elif ch == 99:
                k = "alt-c"
            elif ch == 100:
                k = "alt-d"
            elif ch == 102:
                k = "alt-f"
            else:
                k = None
            stdscr.nodelay(False)

        ###################################################
        state = update_state(state,k,width,height,abbrev_dict)
        
        if outfile:
            with open(outfile, "w+") as f:
                f.write(clean_str(state.text))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        outfile = sys.argv[1]
    else:
        outfile = None
    curses.wrapper(draw_menu)
