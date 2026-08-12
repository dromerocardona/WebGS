import serial
import csv
import time
import threading
import queue
import logging
import json

class Communication ():
    def __init__(self, port, baudrate, csv):
        self.serial_port = port
        self.baud_rate = baudrate
        self.csv_file = csv
        self.running = False