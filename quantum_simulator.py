from qubit import Qubit
from entangled_qubit import EntangledQubit
from gate import HadamardGate, CNOTGate, PauliXGate, PauliYGate, PauliZGate
from quantum_circuit import QuantumCircuit
import time

class QuantumSimulator:
    def __init__(self):
        self.circuit = QuantumCircuit()

        # Add individual qubits
        for _ in range(3):
            self.circuit.add_qubit(Qubit())

        # Add entangled qubits (3-qubit Bell state)
        self.entangled_qubit = EntangledQubit([Qubit(), Qubit(), Qubit()])
        self.circuit.add_qubit(self.entangled_qubit)
        self.setup_gates()

    def setup_gates(self):
        self.circuit.set_gates([
            HadamardGate(),            # Apply Hadamard to Qubit 0
            CNOTGate(),            # CNOT between Qubit 0 and 1
            PauliXGate(),             # Apply Pauli-X to Qubit 1
            PauliYGate(),             # Apply Pauli-Y to Qubit 2
            HadamardGate(),           # Apply Hadamard to the entangled qubit
        ] ,
        [
            [0], [0,1], [2], [3], [2]
        ]
        
        )

    def run(self):
        print("\n--- Initial States ---")
        for qubit in self.circuit.get_qubits():
            print(qubit)

        print("\n--- Applying Gates ---")
        self.circuit.apply_all_gates()

        print("\n--- Final States ---")
        for qubit in self.circuit.get_qubits():
            print(qubit)

        print("\n--- Measuring All Qubits ---")
        for idx, qubit in enumerate(self.circuit.get_qubits()):
            if isinstance(qubit, EntangledQubit):
                print(f"Entangled Qubit Measurement: {qubit.measure()}")
            else:
                print(f"Qubit {idx} Measurement: {qubit.measure()}")
