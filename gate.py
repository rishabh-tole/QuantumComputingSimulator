from abc import ABC, abstractmethod
import numpy as np

class Gate(ABC):
    @abstractmethod
    def apply(self, state, qubit_indices):
        pass

    @abstractmethod
    def get_matrix(self):
        pass
