from quantum_state import QuantumState

class QuantumCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def add_qubit(self, qubit):
        self.qubits.append(qubit)

    def set_gates(self, gates, qubit_indices):

        self.gates = []
        for i in range(len(gates)):
            self.gates.append((gates[i], qubit_indices[i]))\

    def apply_all_gates(self):
        state = QuantumState(self.qubits)
        for gate, qubit_indices in self.gates:
            gate.apply(state, qubit_indices)

    def measure_all(self):
        return QuantumState(self.qubits).measure()
