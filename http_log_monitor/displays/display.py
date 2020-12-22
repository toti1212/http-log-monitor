from threading import Thread


class Display(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def show_data(self, data):
        NotImplemented
