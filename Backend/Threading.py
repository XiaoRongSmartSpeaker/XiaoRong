from threading import Thread, Event

# target: function name
# name: threading name
# args: function parameter


class Job(Thread):
    def __init__(self, main, name, func, args, daemon=False):
        super(Job, self).__init__(name=name,
                                  target=func,
                                  args=args,
                                  daemon=daemon)
        # threading basic info
        self.name = name
        self.func = func.__name__
        self.args = args
        self.result = None

        # threading control parameter
        self.__main_proc = main
        self.__running = Event()
        self.__unlock = Event()
        self.__resume = Event()
        self.__running.clear()
        self.__unlock.set()
        self.__resume.set()

        print("Thread '", name, "' setup successfully.", sep='')

    def reset(self) -> None:
        self.__running.clear()
        self.__unlock.set()
        self.__resume.set()

    def run(self) -> None:
        if self.__unlock.is_set():
            self.__running.set()
            super(Job, self).run()
        else:
            self.__unlock.wait()
            self.__running.set()
            super(Job, self).run()

    def add_thread(self, func_info) -> None:
        self.__main_proc.add_thread(func_info)

    def get_instance(self, class_name) -> object:
        return self.__main_proc.get_instance(class_name)

    def check_info(self):
        print(
            "Thread ",
            self.name,
            " running is ",
            True if self.__running.is_set() else False,
            sep='')
        print(
            "Thread ",
            self.name,
            " unlock is ",
            True if self.__unlock.is_set() else False,
            sep='')
        print(
            "Thread ",
            self.name,
            " pause is ",
            True if self.__pause.is_set() else False,
            sep='')
        return True if self.__running.is_set() else False
        
    def is_run(self) -> bool:
        return True if self.__running.is_set() else False

    def is_pause(self) -> bool:
        return False if self.__resume.is_set() else True

    def wait_for_exec(self) -> None:
        self.__resume.wait()

    def pause(self) -> None:
        self.__resume.clear()

    def resume(self) -> None:
        self.__resume.set()

    def lock(self) -> None:
        self.__unlock.clear()

    def unlock(self) -> None:
        self.__unlock.set()
