import numpy as np
from abc import ABC, abstractmethod

class Gate(ABC):
    @abstractmethod
    def apply(self, state, qubit_indices):
        pass

    @abstractmethod
    def get_matrix(self):
        pass


class CNOTGate(Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])


class HadamardGate(Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return np.array([
            [1 / np.sqrt(2), 1 / np.sqrt(2)],
            [1 / np.sqrt(2), -1 / np.sqrt(2)]
        ])


class PauliXGate(Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return np.array([
            [0, 1],
            [1, 0]
        ])


class PauliYGate(Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return np.array([
            [0, -1j],
            [1j, 0]
        ])


class PauliZGate(Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return np.array([
            [1, 0],
            [0, -1]
        ])
