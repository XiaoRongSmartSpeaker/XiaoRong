import os
import queue
import time

from Threading import Job
from importlib import import_module

feature_path = './feature'

class Main():
    def __init__(self) -> None:
        self.threads = []                           # current running thread
        self.__data_que = queue.Queue()             # pending data
        self.feature_list = []                      # imported class
        self.__declare_class = []                   # declared class
        self.__pending_threads = queue.Queue()      # pending thread info
        self.__DAEMON_THREAD = [                    # define daemon work
            'voice_to_text'
        ]
    
    def add_thread(self, func_info) -> None:
        self.__pending_threads.put(func_info)

    def open_thread(self) -> None:
        func_info = self.__pending_threads.get()

        for dec_class in self.__declare_class:
            if dec_class['name'] == func_info['name']:
                try:
                    func = getattr(dec_class['class'], func_info['func'])
                    args = func_info['args'] if 'args' in func_info else ()

                    # judge whether this work is daemon feature or not
                    if func_info['func'] in self.__DAEMON_THREAD:
                        self.threads.append(Job(self, func_info['name'], func, args))
                    else:
                        self.threads.append(Job(self, func_info['name'], func, args, True))

                    self.threads[-1].start()
                    return
                except:
                    print('Could not find method', func_info['func'])
                    return


        for feature in self.feature_list:
            if feature['name'] == func_info['class']:
                # initial class instance
                class_entity = feature['class']()
                self.__declare_class.append({
                    'name': func_info['class'],
                    'instance': class_entity
                })
                # get the class method address
                try:
                    func = getattr(class_entity, func_info['func'])

                    # judge whether this work is daemon feature or not
                    if func_info['func'] in self.__DAEMON_THREAD:
                        self.threads.append(Job(self, func_info['class'], func, func_info['args']))
                    else:
                        self.threads.append(Job(self, func_info['class'], func, func_info['args'], True))
                    
                    self.threads[-1].start()
                    return
                except:
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

def reciprocal(num):
    for n in range(num, 0, -1):
        print(n, 'seconds')
        time.sleep(1)

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
            module = import_module(feature_path.replace('./', '') + '.' + feature)
            try:
                # from feature module get class object
                class_entity = getattr(module, feature)
                feature_obj = {
                    'class': class_entity,
                    'name': feature
                }
                main.feature_list.append(feature_obj)
            except:
                print('import class instance error')
                continue
        except:
            print('import module python file error')
            continue

    # initial speaker feature
    main.add_thread({
        'class': 'vioce_to_text',
        'func': 'voice_to_text',
        'args': ()
    })
    main.open_thread()
    main.add_thread({
        'class': 'monitering',
        'func': 'monitering',
    })
    main.open_thread()
    
    while True:
        # clear that completed threading
        for i in range(0, len(main.threads)):
            if not main.threads[i].is_alive():
                del main.threads[i]

        # if there are pending thread data
        if not main.threading_empty():
            main.open_thread()