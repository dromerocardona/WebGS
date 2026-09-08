from data import Data
from communication import Communication
import signal

class WebGroundStation:
    def __init__(self):
        print("Initializing Web Ground Station...")
        self.data = Data()

        self.data.load() # Load configuration data

        self.communication = Communication(self.data.config['port'], self.data.config['baudrate'], self.data.config['csv'])
        
        signal.signal(signal.SIGINT, self.communication.stop)

if __name__ == "__main__":
    gs = WebGroundStation()