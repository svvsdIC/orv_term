import serial
import queue
from contextlib import contextmanager


def serial_port_list():
    ser_list = serial.tools.list_ports.comports()
    # TODO sort and add 'loop://'
    return ser_list

@contextmanager
def open_port(serial_port_url, baudrate):
    # open the serial port
    port = serial.serial_for_url(serial_port_url, baudrate)

    #todo: check for exeption when not able to open


    #create read/write queues
    rx_q = queue.Queue()
    tx_q = queue.Queue()

    # Launch rx/tx threads

    #yield queues for application use
    yield rx_q, tx_q


    tx_q.join()
    rx_q.join()

    pass


