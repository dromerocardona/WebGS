from data import Data
from server import Server
from communication import Communication

class WebGroundStation:
    def __init__(self):
        print("Initializing Web Ground Station...")
        self.server = Server()
        self.data = Data()

        self.data.load() # Load configuration data

        self.communication = Communication(self.data.config['port'], self.data.config['baudrate'], self.data.config['csv'])

if __name__ == "__main__":
    gs = WebGroundStation()