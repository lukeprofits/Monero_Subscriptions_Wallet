from abc import ABC, abstractmethod

class View(ABC):
    def __init__(self, app):
        self._app = app
        self._elements = []

    def add(self, element):
        self._elements.append(element)
        return element

    def destroy(self):
        for element in self._elements:
            element.destroy()
        self._elements = []

    @abstractmethod
    def build(self):
        pass