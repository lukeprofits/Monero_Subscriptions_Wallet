from abc import ABC, abstractmethod
from src.interfaces.observer import Observer

"""
The Notifier interface provides functions for managing observers.
"""

class Notifier(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass