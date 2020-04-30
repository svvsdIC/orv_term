import serial
import queue
import threading
from contextlib import contextmanager
from contextlib import closing


def serial_port_list():
    ser_list = serial.tools.list_ports.comports()
    # TODO sort and add 'loop://'
    return ser_list

def rx_loop(serial_port, rx_q):
    import itertools
    import time
    c = itertools.count()
    while True: # check event state
        print(f'rx {next(c)}')
        time.sleep(0.1)

def tx_loop(serial_port, tx_q):
    import itertools
    import time
    c = itertools.count()
    while True:
        print(f'tx {next(c)}')
        time.sleep(0.1)

@contextmanager
def open_port(serial_port_url, baudrate):
    # open the serial port
    with closing(serial.serial_for_url(serial_port_url, baudrate)) as serial_port:
        # create read/write queues
        rx_q = queue.Queue()
        tx_q = queue.Queue()

        # launch RX and TX worker threads
        rx_end = threading.Event()
        rx_loop.rx_end = rx_end
        rx_thread = threading.Thread(target=rx_loop, args(serial_port, rx_q))

        tx_end = threading.Event()
        tx_loop.tx_end = tx_end
        tx_thread = threading.Thread(target=tx_loop, args(serial_port, tx_q))

def stop_rxtx_loops():
    pass
    # sset stop events






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

# TODO: Things to check
#   * raise exception if not valid device, how does open work when file not found?
#   * how system behaves when exexptions are raised from my code
#   * Is there any way for threads to not terminate?
#   ** mark task done on queue receive data
#   * add logging


