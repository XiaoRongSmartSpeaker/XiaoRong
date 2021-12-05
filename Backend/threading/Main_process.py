from _typeshed import HasFileno
import queue
import threading

from Threading import Job

class Main():
    def __init__(self):
        self.threads = []
        self.data_que = queue.Queue()
        self.__

    def add_thread(self, class_name, func_name, args):
        self.threads.append(Job(class_name, func_name, args))

    def send(self, data):
        self.data_que.put(data)

if __name__ == "__main__":
    main = Main()
    
    while True:
        for thread in main.threads:
            if thread.is_run():
                continue
            else:
                thread.start()
                break
        

        if not main.data_que.empty():
            send_data = main.data_que.get()
            for thread in main.threads:
                if thread.getName() == send_data.name:
                    thread.receve(send_data)
                    break