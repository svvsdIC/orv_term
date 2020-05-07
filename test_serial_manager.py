#import unittest
import logging
import serial_manager

def test_serial_port_list():
    for s in serial_manager.serial_ports():
        print(f'{s}')
        print(f'{s!r}')


def test_serial_manager_loopback_url():
    with serial_manager.SerialManager('loop://', 115200) as sm:
        rx_q, tx_q = sm.queues


        while True:
            # perform read/write
            tx_q.put(b'1234\n')
            b = rx_q.get()

            assert b == b'1234\n'

            # send signals to stop threads
            #sm.signal_stop()

    # on context exit threads end and join to the main thread
    # serial port is closed


def test_serial_manager_serial_info_loopback():
    ports = serial_manager.serial_ports()

    # find loopback from list
    loopback_device = None


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    test_serial_port_list()

    test_serial_manager_loopback_url()
    test_serial_manager_serial_info_loopback()
