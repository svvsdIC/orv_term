import serial
import serial.tools.list_ports
import queue
import threading
import logging
from operator import attrgetter
from collections import namedtuple

# TODO: Things to check
#   * raise exception if not valid device, how does open work when file not found?
#   * how system behaves when exceptions are raised from my code
#   * Is there any way for threads to not terminate?
#   * add logging
#   * __all__ or __slot__
#   * what thread are left running if a thread raises an exception
#   * add thread exception handler

__all__ = (
    'serial_ports',
    'SerialManager',
)

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
        self.port = serial_port

        # Create thread ending notification event
        self.end_loop = threading.Event()

        # Create queue to pass to application data read from serial port
        self.q = queue.SimpleQueue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self.end_loop.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)


class TxLoop(threading.Thread):
    def __init__(self, serial_port):
        # Initialize thread structures
        super().__init__()
        self.name = 'TX Loop'

        # Keep a reference to the serial port
        self.port = serial_port

        # Create thread ending notification event
        self.end_loop = threading.Event()

        # Create queue to pass to application data read from serial port
        self.q = queue.SimpleQueue()

    def run(self):
        import itertools
        import time
        c = itertools.count()
        while not self.end_loop.is_set():  # check event state
            print(f'{self.name} {next(c)}')
            time.sleep(0.1)


class SerialManager:
    def __init__(self, serial_device, baudrate):
        # When a user uses the serial_ports() function to search for available
        # devices on the system, it returns SerialInfo objects.  The code can
        # use these directly.
        # When the user provided serial_device does not behave like a SerialInfo
        # then it is safe to assume they know better and use the serial_device
        # as it was passed in.
        serial_url = getattr(serial_device, 'dev', serial_device)
        self._serial = serial.serial_for_url(serial_url, baudrate)
        log.info('Opened serial port %s', self._serial)

        self._rx_thread = RxLoop(self._serial)
        self._tx_thread = TxLoop(self._serial)


    @property
    def queues(self):
        return self._rx_thread.q, self._tx_thread.q

    def signal_stop(self):
        self._rx_thread.end_loop.set()
        self._tx_thread.end_loop.set()

    def __enter__(self):
        self._rx_thread.start()
        self._tx_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Wait for the threads to terminate
        self._rx_thread.join()
        self._tx_thread.join()

        # Clean up open resources
        self._serial.close()
