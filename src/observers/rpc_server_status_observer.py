from src.interfaces.observer import Observer

class RPCServerStatusObserver(Observer):
    def __init__(self, label):
        self.label = label

    def update(self, subject):
        self.label.configure(text=subject.status_message)
