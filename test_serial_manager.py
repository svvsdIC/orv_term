#import unittest
import logging
import serial_manager

def test_serial_port_list():
    for s in serial_manager.serial_ports():
        print(f'{s}')


def test_serial_manager_loopback_url():
    with serial_manager.SerialManager('loop://', 115200) as sm:
        rx_q, tx_q = sm.queues

        # perform read/write
        import time
        time.sleep(5)

        # send signals to stop threads
        sm.signal_stop()

    # on context exit threads end and join to the main thread
    # serial port is closed


def test_serial_manager_serial_info_loopback():
    ports = serial_manager.serial_ports()

    # find loopback from list
    loopback_device = None



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    test_serial_port_list()

    test_serial_manager_loopback_url()
    test_serial_manager_serial_info_loopback()
