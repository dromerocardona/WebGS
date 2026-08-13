import serial
import csv
import time
import threading
import queue
import logging
import json
from serial.tools import list_ports
from server import Server
from data import Data

class Communication ():
    def __init__(self, port, baudrate, csv_file):
        self.serial_port = port
        self.baud_rate = baudrate
        self.csv_file = csv_file
        self.running = False
        self.server = Server()
        self.data = Data()
        
        # Telemetry definition
        self.telemetryDef = self.data.telemetry

        # CSV headers
        self.telemetryHeaders = [field["name"] for field in self.data.telemetry]
        
        # Last telemetry packet
        self.lastTelemetry = {}
        
        # Initialize serial connection
        try:
            self.serial = serial.Serial(self.serial_port, self.baud_rate, timeout=4)
        except serial.SerialException as e:
            logging.error(f"Error initializing serial connection: {e}")
            print(f"Available ports: {list(map(lambda c: c.device, list_ports.comports()))}")
            self.serial = None
            
        # Initialize CSV file
        headers = None
        try:
            with open(self.csv_file, 'r', newline='') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
        except FileNotFoundError:
            headers = None

        # Add headers if they don't exist
        if headers != self.telemetryHeaders:
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.telemetryHeaders)
        
        self.start()
    
    def start(self):
        if self.serial is None:
            logging.error("Serial connection not initialized")
            return
        
        print("Starting communication...")
        
        self.server.start()

        # Start running read/send threads
        self.running = True
        self.readThread = threading.Thread(target=self.read)
        self.readThread.start()
        self.sendThread = threading.Thread(target=self.send)
        self.sendThread.start()
    
    def read(self):
        print("Reading from serial port...")
        while True:
            pass
    
    def send(self):
        print("Ready to send data...")
        while True:
            pass
    
    def stop(self):
        if self.serial:
            self.serial.close()
        if self.readThread:
            self.readThread.join()
        if self.sendThread:
            self.sendThread.join()
            
        self.running = False
        self.flushCSV()
        print("Communication stopped.")
        
    def flushCSV(self):
        """Flush the csv file"""
        with open(self.csv_file, 'a', newline='') as f:
            pass