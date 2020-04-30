import serial
import queue
import threading
from contextlib import contextmanager
from contextlib import closing

class RxLoop(threading.Thread):
    def __init__(self, serial_port):
        # Initialize thread structures
        super().__init__()
        self.name = 'RX Loop'

        # Keep a reference to the serial port
        self._port = serial_port

        # Create thread ending notification event
        self._rx_end = threading.Event()

        # Create queue to pass to application data read from serial port
        self.rx_q = queue.Queue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self._rx_end.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)


class TxLoop(threading.Thread):
    def __init__(self, serial_port):
        # Initialize thread structures
        super().__init__()
        self.name = 'TX Loop'

        # Keep a reference to the serial port
        self._port = serial_port

        # Create thread ending notification event
        self._tx_end = threading.Event()

        # Create queue to pass to application data read from serial port
        self.tx_q = queue.Queue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self._tx_end.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)


def serial_port_list():
    ser_list = serial.tools.list_ports.comports()
    # TODO sort and add 'loop://'
    return ser_list


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
        # Create and launch RX and TX worker threads
        rx_thread = RxLoop(serial_port)
        tx_thread = TxLoop(serial_port)

        rx_thread.start()
        tx_thread.start()

        print()

        # yield queues for application use
        yield rx_thread.rx_q, tx_thread.tx_q

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


