class Test:
    def __init__(self):
        pass
    def get_input_str(self):
        while True:
            # add thread
            self.thread.wait_for_exec()
            zh_text = ""
            try:
                input_str = input("輸入文字指令：")
                self.thread.add_thread({
                    "class": "Extract",
                    "func": "main",
                    "args": (input_str,)
                })
                self.thread.pause()
                print('return', input_str)
            except:
                pass
    def import_thread(self, thread):
        self.thread = thread