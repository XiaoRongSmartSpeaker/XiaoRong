import threading

# target: function name
# name: threading name
# args: function parameter

class Job(threading.Thread):
    def __init__(self, class_name, func_name, args):
        super(Job, self).__init__(  name = class_name,
                                    target = func_name,
                                    args = args,
                                    daemon = True)
        self.__flag = threading.Event()
        self.__running = threading.Event()
        self.__flag.set()
        self.__running.set()
    
    def run(self):
        if self.__running.is_set():
            super(Job, self).run()

    def pause(self):
        self.__running.clear()

    def stop(self):
        self.__flag.clear()
        self.__running.clear()
    
    def resume(self):
        self.__running.set()

    # def send(self, class_name, func_name, args):

