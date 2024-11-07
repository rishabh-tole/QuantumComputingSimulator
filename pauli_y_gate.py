# pauli_y_gate.py
import gate
import numpy as np
from matrix import Matrix

class PauliYGate(gate.Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)
    
    def get_matrix(self):
        return Matrix([[0, -1j], [1j, 0]])
