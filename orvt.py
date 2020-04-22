#!/usr/bin/env python

import sys
import queue
import serial
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum
from threading import Thread
from types import SimpleNamespace

class Messages(Enum):
    WRITEMSG = 1

# controller
def workcycle(guiref, model, queue):
    """
    Fun worker thread

    :param guiref:
    :param model:
    :param queue:
    :return:
    """
    while True:
        msg = queue.get()
        '''Manage the message extracted from the queue'''
        print(msg)
        '''Take care of other tasks, like refreshing the UI with newly received content'''

# view
def gui(root,q):
    """
    Builds the GUI for ORV Term

    :param root:
    :return:
    """

    '''Build a Tkinter GUI'''
    root.title('orvt')
    ttk.Label(root, text='Hello World').pack()
    '''Return a collection of significant widget references'''

    return None


class Orvt(tk.Tk):
    """
    OpenROV serial terminal tester program
    """
    def __init__(self):
        super().__init__()

        self.title('orvt')
        ttk.Label(self, text='Hello World').pack()





def main(serial_port, baudrate):
    #open the serial port
    port = serial.serial_for_url(serial_port, baudrate)

    # Create inter-thread messaging queue
    q = queue.Queue()

    # Create GUI elements
    guiref = gui(root, q)

    # Initialize model application will be working on
    model = SimpleNamespace(port=port)
    orvt = Orvt()

    t = Thread(target=workcycle, args=(guiref, model, q,))
    #t.daemon = True  # daemonize it, so it will die when the program stops
    t.start()

    # Start the Application main loop
    #root.protocol("WM_DELETE_WINDOW", callback)
    orvt.mainloop()

    print('mainloop exited')

    # TODO: send thread termination messages and join
    # wait for a bit, then forcefully end threads

    return 0

if __name__ == '__main__':
    # TODO: add argument parsing
    sys.exit(main('loop://', 115200))
