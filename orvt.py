#!/usr/bin/env python

import sys
import tkinter as tk

def main(serial = None, baudrate = None):
    root = tk.Tk()
    root.title('orvt')
    tk.Label(root, text='Hello World').pack()
    tk.mainloop()
    return 0

if __name__ == '__main__':
    # TODO: add argument parsing
    sys.exit(main())
