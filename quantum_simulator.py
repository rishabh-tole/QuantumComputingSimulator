from quantum_circuit import QuantumCircuit
from qubit import Qubit
from complex import Complex
import time
from hadamard_gate import HadamardGate

# Create the QuantumSimulator class
class QuantumSimulator:
    def __init__(self):
        self.circuit = QuantumCircuit()
        # Add 5 qubits with initial states
        self.circuit.add_qubit(Qubit().set_state(Complex(0.5,0), Complex(0.5,0)))
        self.circuit.add_gate(HadamardGate(), 0)


    def run(self):

        Qubit.display_all_qubits()
        
        time.sleep(2)
        # Apply all other gates and measure qubits
        self.circuit.apply_all_gates()
        time.sleep(2)
        results = self.circuit.measure_all()
        print("Measurement results:", results)
