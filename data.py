import json

class Data:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state

    def load(self):
        print("Loading configuration data...")
        with open("config.json", "r") as f:
            try:
                self.__dict__.update(json.load(f))
            except json.JSONDecodeError as e:
                print(f"Error loading configuration: {e}")
                self.__dict__.update({})  # Load default empty configuration