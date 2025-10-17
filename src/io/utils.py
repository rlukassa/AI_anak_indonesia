import os
import time

class Utils:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def delay(ms):
        time.sleep(ms / 1000)
