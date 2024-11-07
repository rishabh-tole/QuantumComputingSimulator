import gate
import numpy as np
from matrix import Matrix

class HadamardGate(gate.Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)

    def get_matrix(self):
        return Matrix([[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 / np.sqrt(2)]])
