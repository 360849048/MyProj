import time
import threading

def printHi():
    print('hello')

print('?')
threading.Timer(1, printHi).start()