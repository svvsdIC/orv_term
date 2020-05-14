#import unittest
import logging
import itertools
import serial_manager

log = logging.getLogger(__name__)

def test_serial_port_list():
    for s in serial_manager.serial_ports():
        print(f'{s}')
        print(f'{s!r}')


def test_serial_manager_url():
    #with serial_manager.SerialManager('loop://', 115200) as sm:
    with serial_manager.SerialManager('/dev/cu.usbmodem14601', 115200) as sm:
        rx_q, tx_q = sm.queues

        c = itertools.count()
        count = next(c)
        while count != 8:
            # perform read/write
            if not rx_q.empty():
                b = rx_q.get()
                count = next(c)
                log.debug('Queue %s', b)
                tx_q.put(b'1234\n')

        # send signals to stop threads
        sm.signal_stop()

    # on context exit threads end and join to the main thread
    # serial port is closed


def test_serial_manager_serial_info_loopback():
    ports = serial_manager.serial_ports()

    # find loopback from list
    loopback_device = None


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
                        level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    test_serial_port_list()

    test_serial_manager_url()
    #test_serial_manager_serial_info_loopback()
