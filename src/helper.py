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