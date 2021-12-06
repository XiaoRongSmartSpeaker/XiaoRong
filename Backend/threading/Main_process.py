import os
import queue
import time

from Threading import Job
from importlib import import_module

feature_path = './feature'

class Main():
    def __init__(self):
        self.threads = []
        self.data_que = queue.Queue()
        self.feature_list = []

    def add_thread(self, class_name, func_name, args):
        self.threads.append(Job(class_name, func_name, args))

    def send(self, data):
        self.data_que.put(data)

def reciprocal(num):
    for n in range(num, 0, -1):
        print(n, 'seconds')
        time.sleep(1)

if __name__ == "__main__":
    # defination main process
    main = Main()
    
    # initial feature class
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
                continue
        except:
            continue
    
    main.add_thread('main', reciprocal, (20,))

    main.threads[0].check_info()

    main.threads[0].start()

    reciprocal(10)

    main.threads[0].join()

    while False:
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