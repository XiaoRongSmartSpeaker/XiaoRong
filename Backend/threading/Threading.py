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
        self.__running = threading.Event()
        self.__unlock = threading.Event()
        self.__pause = threading.Event()
        self.__running.clear()
        self.__unlock.set()
        self.__pause.clear()
    
    def run(self):
        if self.__unlock.is_set():
            self.__running.set()
            super(Job, self).run()
        else:
            self.__unlock.wait()
            self.__running.set()
            super(Job, self).run()

    def is_run(self):
        return True if self.__running.is_set() else False

    def pause(self):
        self.__pause.set()

    def resume(self):
        self.__pause.clear()

    def lock(self):
        self.__unlock.clear()
    
    def unlock(self):
        self.__unlock.set()

    # def send(self, class_name, func_name, args):

