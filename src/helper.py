import Tkinter as tk

def tk_entry_text(entry, text):
    '''
    set text for an entry in Tkinter
    '''
    state = entry["state"]
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(state=state)
    return

def special_char_to_int(c):
    if c == '0':
        return 0
    elif c == '1':
        return 1
    elif c == 'x' or c == '-' or c=='3':
        return 3
    return -1

def int_to_special_char(i):
    if i == 0:
        return '0'
    if i == 1:
        return '1'
    if i == 3:
        return 'x'
    return '-1'

def int_to_char_to_display(i):
    if i == 0:
        return '0'
    if i == 1:
        return '1'
    if i == 3:
        return '-'
    
    return '-1'