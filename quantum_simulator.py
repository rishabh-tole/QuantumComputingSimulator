from quantum_circuit import QuantumCircuit
from qubit import Qubit
from entangled_qubit import EntangledQubit
from gate import HadamardGate, PauliXGate, PauliYGate, PauliZGate


class QuantumSimulator:
    def __init__(self):
        self.circuit = QuantumCircuit()
        self.entangled = None

    def setup(self):
        # Add 2 individual qubits
        for _ in range(2):
            self.circuit.add_qubit(Qubit())

        # Add an entangled qubit (e.g., Bell State |00⟩ + |11⟩)
        self.entangled = EntangledQubit([Qubit(5,4), Qubit(2,5), Qubit(8,1)])
        self.circuit.add_qubit(self.entangled)

        # Apply gates
        self.circuit.add_gate(HadamardGate(), [0])  # Apply Hadamard to first individual qubit
        self.circuit.add_gate(PauliZGate(), [1])
        self.circuit.add_gate(PauliXGate(), [2])   # Apply Pauli-X to the entangled qubit

    def run(self):

        self.setup()

        print("Initial Qubit States:")
        for qubit in self.circuit.qubits:
            print(qubit)

        self.entangled.display_entangled_state()

        print("\nApplying Gates...")
        self.circuit.apply_all_gates()

        print("\nFinal Qubit States:")
        for qubit in self.circuit.qubits:
            print(qubit)
        self.entangled.display_entangled_state()


        print("\nMeasurements:")
        results = self.circuit.measure_all()
        print(results)

        self.entangled.display_entangled_state()


# Run Simulation
if __name__ == "__main__":
    simulator = QuantumSimulator()
    simulator.run()
