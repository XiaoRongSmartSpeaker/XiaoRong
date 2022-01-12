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

        # threading control parameter
        self.__main_porc = main
        self.__running = Event()
        self.__unlock = Event()
        self.__pause = Event()
        self.__running.clear()
        self.__unlock.set()
        self.__pause.clear()

        print("Thread '", name, "' setup successfully.", sep='')

    def reset(self) -> None:
        self.__running.clear()
        self.__unlock.set()
        self.__pause.clear()

    def run(self) -> None:
        if self.__unlock.is_set():
            self.__running.set()
            super(Job, self).run()
        else:
            self.__unlock.wait()
            self.__running.set()
            super(Job, self).run()

    def add_thread(self, func_info) -> None:
        self.__main_porc.add_thread(func_info)

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

    def is_run(self) -> bool:
        return True if self.__running.is_set() else False

    def pause(self) -> None:
        self.__pause.set()

    def resume(self) -> None:
        self.__pause.clear()

    def lock(self) -> None:
        self.__unlock.clear()

    def unlock(self) -> None:
        self.__unlock.set()
