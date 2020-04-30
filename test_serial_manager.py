#import unittest
from serial_manager import *


if __name__ == '__main__':
    with open_port('loop://', 115200) as (rx, tx):
        print(rx)
        print(tx)
        # time.sleep(10)
        # stop_rxtx_loops()
