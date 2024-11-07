from quantum_state import QuantumState

class QuantumCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def add_qubit(self, qubit):
        self.qubits.append(qubit)

    def add_gate(self, gate, *qubit_indices):
        self.gates.append((gate, qubit_indices))

    def apply_all_gates(self):
        state = QuantumState(self.qubits)
        for gate, qubit_indices in self.gates:
            gate.apply(state, qubit_indices)

    def measure_all(self):
        return QuantumState(self.qubits).measure()
