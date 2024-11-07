import gate
from matrix import Matrix

class PauliXGate(gate.Gate):
    def apply(self, state, qubit_indices):
        state.apply_gate(self.get_matrix(), qubit_indices)
    
    def get_matrix(self):
        return Matrix([[0, 1], [1, 0]])
