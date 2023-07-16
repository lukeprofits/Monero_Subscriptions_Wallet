import threading
class ThreadManager():
    _stop_flag = None
    _update_subscriptions = None
    @classmethod
    def stop_flag(cls):
        if not cls._stop_flag:
            cls._stop_flag = threading.Event()
        return cls._stop_flag

    @classmethod
    def update_subscriptions(cls):
        if not cls._update_subscriptions:
            cls._update_subscriptions = threading.Event()
        return cls._update_subscriptions