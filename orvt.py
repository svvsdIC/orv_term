#!/usr/bin/env python

import sys
import queue
import serial
import tkinter as tk
import tkinter.ttk as ttk

class Orvt(tk.Tk):
    """
    OpenROV serial terminal tester program
    """
    def __init__(self):
        super().__init__()

        self.title('orvt')
        self.resizable(True, True)

        # Layout UI objects
        # self.main_frame = tk.Frame(self, width=500, height=300, bg="lightgrey")

        self.serial_text = tk.Text(self)
        self.serial_text.pack(expand=1, fill=tk.BOTH)
        self.serial_text.pack()
        self.serial_text.config(state=tk.DISABLED)

        self.cmd_entry = ttk.Entry(self)
        self.cmd_entry.pack()


def main(serial_port, baudrate):
    #open the serial port
    port = serial.serial_for_url(serial_port, baudrate)

    # Create inter-thread messaging queue
    q = queue.Queue()

    # Create GUI elements
    orvt = Orvt()

    # Begin running the UI.
    # This function will not return until the Tk application is closed
    orvt.mainloop()

    #clean up
    print('mainloop exited')

    if port.isOpen():
        port.close()

    # TODO: send thread termination messages and join
    # wait for a bit, then forcefully end threads

    return 0

if __name__ == '__main__':
    # TODO: add argument parsing
    sys.exit(main('loop://', 115200))
