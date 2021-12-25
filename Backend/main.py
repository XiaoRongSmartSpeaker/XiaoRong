import os
import time
from queue import Queue

from Threading import Job
from importlib import import_module
from logger import logger

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
            'voice_to_text'
        ]

    def add_thread(self, func_info) -> None:
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
                except BaseException:
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
    # defination main process
    main = Main()

    # import feature class
    feature_list = os.listdir(feature_path)
    for file in feature_list:
        full_filename = os.path.basename(feature_path + '/' + file)
        filename = os.path.splitext(full_filename)

        # if not a python file skip
        if filename[1] != '.py':
            continue
        else:
            feature = filename[0]

        try:
            # import feature module
            module = import_module(
                feature_path.replace(
                    './', '') + '.' + feature)
            try:
                # from feature module get class object
                class_entity = getattr(module, feature)
                feature_obj = {
                    'class': class_entity,
                    'name': feature
                }
                print('import class instance successfully')
                main.feature_list.append(feature_obj)
                # initialize instance corresponding thread
                main.instance_thread_correspond[feature] = []
            except BaseException:
                print('import class instance error')
                continue
        except BaseException:
            print('import module python file error')
            continue

    # initial speaker feature
    main.add_thread({
        'class': 'voice_to_text',
        'func': 'voice_to_text',
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
        main.threads.reverse()
        for thread in main.threads:
            if not thread.is_alive():
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

        # if there are pending thread data
        if not main.threading_empty():
            main.open_thread()
