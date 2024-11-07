from quantum_circuit import QuantumCircuit
from qubit import Qubit
from complex import Complex
import time
from hadamard_gate import HadamardGate
from pauli_x_gate import PauliXGate
from pauli_y_gate import PauliYGate
from pauli_z_gate import PauliZGate
import random

# Create the QuantumSimulator class
class QuantumSimulator:
    def __init__(self):
        self.circuit = QuantumCircuit()
        # Add 5 qubits with initial states
        # self.circuit.add_qubit(Qubit().set_state(Complex(0.5,0), Complex(0.5,0)))

        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
        self.circuit.add_qubit(Qubit().set_state(Complex(random.uniform(0, 1), random.uniform(0, 1)), Complex(random.uniform(0, 1), random.uniform(0, 1))))
    
        self.circuit.add_gate(PauliXGate(), [i for i in range(9)])


    def run(self):

        Qubit.display_all_qubits()
        
        time.sleep(2)
        # Apply all other gates and measure qubits
        self.circuit.apply_all_gates()

        time.sleep(2)

        Qubit.display_all_qubits()
        results = self.circuit.measure_all()

        Qubit.display_all_qubits()
        print("Measurement results:", results)
