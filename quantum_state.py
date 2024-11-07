import numpy as np

class QuantumState:
    def __init__(self, qubits):
        self.qubits = qubits
        self.state_vector = self._initialize_state_vector()

    def _initialize_state_vector(self):
        vector = np.array([1])
        for qubit in self.qubits:
            vector = np.kron(vector, qubit.get_state())
        return vector

    def apply_gate(self, gate_matrix, qubit_indices):
        for idx in qubit_indices:
            self.state_vector = gate_matrix.apply_to_vector(self.state_vector)

    def measure(self):
        return [qubit.measure() for qubit in self.qubits]

    def normalize(self):
        norm = np.linalg.norm(self.state_vector)
        self.state_vector = self.state_vector / norm
