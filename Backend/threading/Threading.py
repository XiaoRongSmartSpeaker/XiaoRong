from threading import Thread, Event

# target: function name
# name: threading name
# args: function parameter

class Job(Thread):
    def __init__(self, class_name, func_name, args):
        super(Job, self).__init__(  name = class_name,
                                    target = func_name,
                                    args = args)
        self.__running = Event()
        self.__unlock = Event()
        self.__pause = Event()
        self.__running.clear()
        self.__unlock.set()
        self.__pause.clear()

        print("Thread '", class_name, "' setup successfully.", sep='')
    
    def run(self):
        if self.__unlock.is_set():
            self.__running.set()
            super(Job, self).run()
        else:
            self.__unlock.wait()
            self.__running.set()
            super(Job, self).run()

    def check_info(self):
        name = super(Job, self).getName()
        print("Thread ", name, " running is ", True if self.__running.is_set() else False, sep='')
        print("Thread ", name, " unlock is ", True if self.__unlock.is_set() else False, sep='')
        print("Thread ", name, " pause is ", True if self.__pause.is_set() else False, sep='')

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

