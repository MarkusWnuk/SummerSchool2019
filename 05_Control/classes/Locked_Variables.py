from threading import Lock

class Scale_Value:

    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def read_value(self):
        self.lock.acquire()
        output = self.value
        self.lock.release()
        return output

    def write_value(self, inputvalue):
        self.lock.acquire()
        self.value = inputvalue
        self.lock.release()