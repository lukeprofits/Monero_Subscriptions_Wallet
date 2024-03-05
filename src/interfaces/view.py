from abc import ABC, abstractmethod

class View(ABC):
    _elements = []

    def add(self, element):
        self._elements.append(element)
        return element

    def destroy(self):
        for element in self._elements:
            element.destroy()

    @abstractmethod
    def build(self):
        pass