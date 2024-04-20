#!/usr/bin/env python3
import sys
import re
from tkinter import *

def copy_to_clipboard():
    txt = T.get('1.0',END)
    root.clipboard_clear()
    root.clipboard_append(txt)
    root.update()
    # with open(clipboard_filename, "w+") as f:
    #     f.write(txt)

def final_tidyup_buffer():
    txt = T.get('1.0',END)
    for i in range(10):
        txt = txt.replace("  "," ")
    txt = txt.replace("\n","")
    txt = txt[:-1] if len(txt) > 0 and txt[-1] == ' ' else txt
    T.delete('1.0', END)
    T.insert(INSERT, txt)

def check_for_alias(event):
    txt = T.get('1.0', INSERT)
    txt = txt.replace("\n","")
    if txt:
        # words = txt.split(' ')
        words = re.split("(\w+)", txt)
        # print(words)
        words = [ w for w in words if w ]
        if words[-1] in replace_dict:
            words[-1] = replace_dict[words[-1]].replace("<CR>","\n").replace("<cr>","\n")
            txt = ''.join(words)
            # print(txt)
            T.delete('1.0', INSERT)
            T.insert(INSERT, txt)

def control_w(event):
    txt = T.get('1.0', INSERT)
    words = txt.split(' ')
    if not words[-1] or words[-1] == "\n":
        words = words[:-1]
    txt = ' '.join(words[:-1]) + ' '
    T.delete('1.0', INSERT)
    T.insert(INSERT, txt)

def control_u(event):
    T.delete('1.0',INSERT)

def control_k(event):
    T.delete(INSERT,END)

def control_a(event):
    T.mark_set("insert", "%d.%d" % (1,0))
    return 'break'  # Cancel the event of selecting the whole body of text

def control_e(event):
    T.mark_set("insert", "%d.%d" % (1,len(T.get('1.0',END))))

def alt_b(event):
    txt_b4 = T.get('1.0',INSERT)
    old_pos = len(txt_b4)
    count = 1
    for c in reversed(txt_b4[:-1]):
        count += 1
        if not c.isalnum():
            break
    T.mark_set("insert", "%d.%d" % (1,old_pos-count+1))

def alt_f(event):
    txt_bef = T.get('1.0',INSERT)
    txt_aft = T.get(INSERT,END)
    old_pos = len(txt_bef)
    count = 1
    for c in txt_aft[1:]:
        count += 1
        if not c.isalnum():
            break
    T.mark_set("insert", "%d.%d" % (1,old_pos+count-1))

def alt_d(event):
    txt_bef = T.get('1.0',INSERT)
    txt_aft = T.get(INSERT,END)
    count = 1
    for c in txt_aft[1:]:
        count += 1
        if not c.isalnum():
            break
    new_txt = ' ' + txt_aft[(count-1):]
    T.delete(INSERT,END)
    T.insert(END, new_txt)
    T.mark_set("insert", "%d.%d" % (1,len(txt_bef)+1))

def alt_c(event):
    curpos = len(T.get('1.0',INSERT))
    in_txt = T.get('1.0',END)
    if in_txt:
        convert_to_upper = in_txt[0].islower()

        sentence_start = True
        out_txt = ""
        for c in in_txt:
            if convert_to_upper:
                out_txt += c.upper() if sentence_start else c
            else:
                out_txt += c.lower() if sentence_start else c

            if c in ['.','!','?'] and not sentence_start:
                sentence_start = True
            elif c in [' ']:
                sentence_start = sentence_start
            elif sentence_start:
                sentence_start = False

        T.delete('1.0',END)
        T.insert(END,out_txt)
        T.mark_set("insert", "%d.%d" % (1,curpos))

def sys_exit(event):
    check_for_alias(event)
    final_tidyup_buffer()
    copy_to_clipboard()
    # sys.exit(0)

with open(sys.argv[1],'r') as f:
    lines = [ line.strip() for line in f]
    replace_dict = dict([ (line.split(' ')[1],' '.join(line.split(' ')[2:])) for line in lines])

root = Tk()
T = Text(root, height=3, width=50, bg="#1F1F1F", fg="#77EE77", insertbackground="#AAFF00", font=("Courier New", 10))
T.config(state=NORMAL)
T.pack(expand=True, fill=BOTH)

for i in ["space","exclam","quotedbl","numbersign","dollar","percent","ampersand","quoteright","parenleft","parenright","asterisk","plus","comma","minus",\
          "period","slash","slash","colon","semicolon","less","equal","greater","question","at","bracketleft","backslash","bracketright","asciicircum","underscore","quoteleft","Tab"]:
    T.bind('<'+i+'>', check_for_alias)

T.bind('<Control-u>', control_u)
T.bind('<Control-k>', control_k)
T.bind('<Control-w>', control_w)
T.bind('<Control-a>', control_a)
T.bind('<Control-e>', control_e)
T.bind('<Alt-b>', alt_b)
T.bind('<Alt-f>', alt_f)
T.bind('<Alt-d>', alt_d)
T.bind('<Alt-c>', alt_c)

T.bind('<Control-q>', sys_exit)
T.bind('<Return>', sys_exit)
T.bind('<Linefeed>', sys_exit)
T.bind('<KP_Enter>', sys_exit)
T.bind('<Control-j>', sys_exit)
T.bind('<Escape>', sys_exit)

T.focus()

mainloop()
