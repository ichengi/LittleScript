# 管理线程模板
class Concur(threading.Thread):
    def __init__(self):
        super(Concur, self).__init__()
        self.iterations = 0
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

    def run(self):
        self.paused = False
        # self.state.notify()  # Unblock self if waiting.s
        do_something()

    def resume(self):  # 用来恢复/启动run
        with self.state:  # 在该条件下操作
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):  # 用来暂停run
        with self.state:  # 在该条件下操作
            self.paused = True  # Block
