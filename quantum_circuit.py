from quantum_state import QuantumState

class QuantumCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def add_qubit(self, qubit):
        self.qubits.append(qubit)

    def get_qubits(self):
        return self.qubits

    def set_gates(self, gates, indices):
        self.gates = [(gates[i], indices[i]) for i in range(len(gates))]

    def apply_all_gates(self):
        quantum_state = QuantumState(self.qubits)
        for gate, qubit_indices in self.gates:
            quantum_state.apply_gate(gate.get_matrix(), qubit_indices)
