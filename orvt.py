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

        self.comms_log = tk.Text(self, wrap=tk.NONE)
        self.comms_log.pack(expand=1, fill=tk.BOTH)
        self.comms_log.pack()
        self.comms_log.config(state=tk.DISABLED)

        self.cmd_entry = ttk.Entry(self)
        self.cmd_entry.bind('<Key-Return>', self.send_cmd)
        self.cmd_entry.bind('<Key-KP_Enter>', self.send_cmd)
        self.cmd_entry.pack()

    def send_cmd(self, event):
        print(f'contents: {event!r}')
        cmd_str = self.cmd_entry.get()
        print(f'{cmd_str}')

        # append to the log
        self.comms_log.config(state=tk.NORMAL)
        self.comms_log.insert(tk.END, cmd_str)
        self.comms_log.insert(tk.END, '\n')
        self.comms_log.config(state=tk.DISABLED)

        # clear the command entry widget
        self.cmd_entry.delete(0, tk.END)





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
