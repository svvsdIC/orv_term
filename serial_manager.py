import serial
import queue
from contextlib import contextmanager
from contextlib import closing


def serial_port_list():
    ser_list = serial.tools.list_ports.comports()
    # TODO sort and add 'loop://'
    return ser_list

@contextmanager
def open_port(serial_port_url, baudrate):
    # open the serial port
    with closing(serial.serial_for_url(serial_port_url, baudrate)) as serial_port:
        # create read/write queues
        rx_q = queue.Queue()
        tx_q = queue.Queue()


    raise ValueError()

    #todo: check for exception when not able to open

    # raise exception if not valid device, how does open work when file not found?



    # Launch rx/tx threads

    #yield queues for application use
    yield rx_q, tx_q

    # block until queues have been serviced,
    # is this necessary if threads have consumed all data?
    tx_q.join()
    rx_q.join()
    #is this okay if GUI has been terminated and therefore cannot consume?  We could consume to nothing instead

    # terminate threads
    # join rx/tx threads
    pass


