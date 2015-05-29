import Tkinter as tk
from view import *

def main():
    root = tk.Tk()
    kmv = KMapView(root)
    root.mainloop()

if __name__ == '__main__':
    main()