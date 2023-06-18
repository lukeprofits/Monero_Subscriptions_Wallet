import threading
class ThreadManager():
    _stop_flag = None
    @classmethod
    def stop_flag(cls):
        if not cls._stop_flag:
            cls._stop_flag = threading.Event()
        return cls._stop_flag