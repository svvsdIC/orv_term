#import unittest
import serial_manager as sm


if __name__ == '__main__':
    with sm.open_port('loop://', 115200) as (rx, tx):
        print(rx)
        print(tx)
