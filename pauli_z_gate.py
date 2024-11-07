# pauli_z_gate.py
import gate
from matrix import Matrix

class PauliZGate(gate.Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)
    
    def get_matrix(self):
        return Matrix([[1, 0], [0, -1]])
