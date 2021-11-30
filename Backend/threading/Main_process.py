import queue
import threading

from Threading import Job

class Main():
    def __init__(self):
        self.threads = []
        self.data_que = queue.Queue()

    def add_thread(self, class_name, func_name, args):
        self.threads.append(Job(class_name, func_name, args))
        self.threads[-1].start()

    def send(self, data):
        self.data_que.put(data)

if __name__ == "__main__":
    