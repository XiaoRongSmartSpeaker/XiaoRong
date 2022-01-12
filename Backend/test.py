import time
import sys
import inspect
from queue import Queue

from Threading import Job
from logger import logger
from dotenv import load_dotenv

# log setting
log = logger.setup_applevel_logger(file_name='./log/smartspeaker.log')

feature_path = './feature'


class Main():
    def __init__(self) -> None:
        self.threads = []                           # current running thread
        self.__data_que = Queue()                   # pending data
        self.feature_list = []                      # imported classes
        self.declare_class = []                     # declared classes
        self.instance_thread_correspond = {}        # instance corresponding thread
        self.__pending_threads = Queue()            # pending thread info
        self.__DAEMON_THREAD = [                    # define daemon work
            'get_input_str'
        ]

    def add_thread(self, func_info) -> None:
        if 'args' in func_info and not isinstance(func_info['args'], tuple):
            func_info['args'] = (func_info['args'],)
        
        self.__pending_threads.put(func_info)

    def open_thread(self) -> None:
        func_info = self.__pending_threads.get()

        for dec_class in self.declare_class:
            if dec_class['name'] == func_info['class']:
                try:
                    func = getattr(dec_class['instance'], func_info['func'])
                    args = func_info['args'] if 'args' in func_info else ()

                    # judge whether this work is daemon feature or not
                    if func_info['func'] in self.__DAEMON_THREAD:
                        new_job = Job(
                            self, func_info['class'], func, args, True)
                    else:
                        new_job = Job(self, func_info['class'], func, args)

                    if getattr(
                        dec_class['instance'],
                        'import_thread',
                            None) is not None:
                        dec_class['instance'].import_thread(new_job)
                        print(
                            self.instance_thread_correspond[func_info['class']])
                        self.instance_thread_correspond[func_info['class']].append(
                            new_job)

                    self.threads.append(new_job)
                    self.threads[-1].start()
                    return
                except BaseException:
                    print('Could not find method', func_info['func'])
                    return

        for feature in self.feature_list:
            if feature['name'] == func_info['class']:
                # initial class instance
                class_entity = feature['class']()
                self.declare_class.append({
                    'name': func_info['class'],
                    'instance': class_entity
                })
                # get the class method address
                try:
                    func = getattr(class_entity, func_info['func'])
                    args = func_info['args'] if 'args' in func_info else ()

                    # judge whether this work is daemon feature or not
                    if func_info['func'] in self.__DAEMON_THREAD:
                        new_job = Job(
                            self, func_info['class'], func, args, True)
                    else:
                        new_job = Job(self, func_info['class'], func, args)

                    if getattr(
                        class_entity,
                        'import_thread',
                            None) is not None:
                        class_entity.import_thread(new_job)
                        self.instance_thread_correspond[func_info['class']].append(
                            new_job)

                    self.threads.append(new_job)
                    self.threads[-1].start()
                    return
                except BaseException as e:
                    print(e)
                    print('Could not find method', func_info['func'])
                    return

        print('Could not find the feature instance', func_info['class'])

    def threading_empty(self) -> bool:
        return True if self.__pending_threads.empty() else False

    def data_empty(self) -> bool:
        return True if self.__data_que.empty() else False

    def send(self, data) -> None:
        self.__data_que.put(data)

    def close(self) -> None:
        for thread in self.threads:
            if not thread.isDaemon():
                thread.join()


if __name__ == "__main__":
    # load env
    load_dotenv(override=True)

    # defination main process
    main = Main()

    # import feature class
    import feature
    featureClasses = inspect.getmembers(
        sys.modules[feature.__name__], inspect.isclass)
    for featureClass in featureClasses:
        try:
            feature_obj = {
                'class': featureClass[1],
                'name': featureClass[0]
            }
            print('import class instance successfully')
            main.feature_list.append(feature_obj)
            # initialize instance corresponding thread
            main.instance_thread_correspond[feature_obj['name']] = []
        except BaseException:
            print('import class instance failed')

    # initial speaker feature
    main.add_thread({
        'class': 'Test',
        'func': 'get_input_str',
    })
    main.open_thread()
    main.add_thread({
        'class': 'monitering',
        'func': 'monitering',
    })
    main.open_thread()

    while True:
        # check every second
        time.sleep(1)

        # clear that completed threading
        # because newer threads are at the back of list
        threading_running = False
        main.threads.reverse()
        for thread in main.threads:
            if not thread.is_alive():
                threading_running = True
                if len(main.instance_thread_correspond[thread.name]) != 0:
                    # discard the last one thread on a feature instance
                    main.instance_thread_correspond[thread.name].pop()

                # get the previous one thread on a feature instance
                try:
                    last_thread = main.instance_thread_correspond[thread.name][-1]
                except BaseException:
                    last_thread = None

                # search instance and update thread pointer
                for dec_class in main.declare_class:
                    if dec_class['name'] == thread.name:
                        if getattr(
                            dec_class['name'],
                            'import_thread',
                                None) is not None:
                            dec_class['name'].import_thread(last_thread)
                        break

                # delete thread
                print('delete thread', thread)
                main.threads.remove(thread)

        main.threads.reverse()

        # if there is no thread alive, open voice to text feature
        if not threading_running:
            main.instance_thread_correspond["Test"][-1].resume()

        # if there are pending thread data
        if not main.threading_empty():
            # open feature and pause voice to text
            main.instance_thread_correspond["Test"][-1].pause()
            main.open_thread()
