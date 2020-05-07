import serial
import serial.tools.list_ports
import queue
import threading
import logging
from operator import attrgetter
from collections import namedtuple
from contextlib import contextmanager
from contextlib import closing


# TODO: Things to check
#   * raise exception if not valid device, how does open work when file not found?
#   * how system behaves when exceptions are raised from my code
#   * Is there any way for threads to not terminate?
#   * add logging
#   * __all__ or __slot__
#   * what thread are left running if a thread raises an exception
#   * add thread exception handler

log = logging.getLogger(__name__)

class SerialInfo(namedtuple('SerialInfo',
                            field_names=('dev', 'description', 'vid', 'pid'),
                            defaults=(None, None, None),
                            )):
    __slots__ = ()
    def __str__(self):
        info_str_parts = list()
        info_str_parts.append(self.dev)
        if self.description is not None:
            info_str_parts.append(f'({self.description})')
        if self.vid is not None and self.pid is not None:
            info_str_parts.append(f'[{self.vid:04x}:{self.pid:04x}]')
        return ' '.join(info_str_parts)


def serial_ports():
    # Always include the loopback device
    yield SerialInfo('loop://', description='PySerial loopback')

    # Look for serial ports on the system
    ports = serial.tools.list_ports.comports()
    ports.sort(key=attrgetter('device'))

    log.debug('Found %d serial ports on the system', len(ports))

    for s in ports:
        yield SerialInfo(s.device,
                         None if s.description == 'n/a' else s.description,
                         s.vid,
                         s.pid)


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
        self.rx_q = queue.SimpleQueue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self._rx_end.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)

    def stop(self):
        self._rx_end.set()


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
        self.tx_q = queue.SimpleQueue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self._tx_end.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)

    def stop(self):
        self._tx_end.set()


@contextmanager
def open_port(serial_port_url, baudrate):
    # open the serial port
    # TODO: ensure that closing decorator actually closes serial port
    with closing(serial.serial_for_url(serial_port_url, baudrate)) as serial_port:
        # Create and launch RX and TX worker threads
        rx_thread = RxLoop(serial_port)
        tx_thread = TxLoop(serial_port)

        rx_thread.start()
        tx_thread.start()

        print()

        # yield queues for application use
        yield rx_thread.rx_q, tx_thread.tx_q

        # stop the threads
        rx_thread.stop()
        tx_thread.stop()

        # terminate threads
        # join rx/tx threads
        pass

def close_port():
    print('stopping threads')
    print(threading.enumerate())

