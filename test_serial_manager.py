#import unittest
import logging
import serial_manager as sm

def test_serial_port_list():
    for s in sm.serial_ports()
        print(f'{s}')

if __name__ == '__main__':
    with sm.open_port('loop://', 115200) as (rx, tx):
        print(rx)
        print(tx)
    logging.basicConfig(level=logging.DEBUG)

        import time
        time.sleep(10)

        sm.close_port()
