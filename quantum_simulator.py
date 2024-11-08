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


        for qubit in self.circuit.get_qubits():
            print(qubit)

    def run(self):
        # Display initial state
        Qubit.display_all_qubits()
        
        time.sleep(2)
        gates = [PauliYGate()]
        gate_indicies = [[i for i in range(9)]]
        self.circuit.set_gates(gates, gate_indicies)
        self.circuit.apply_all_gates()
        Qubit.display_all_qubits()

        time.sleep(2)
        gates = [PauliZGate()]
        gate_indicies = [[i for i in range(9)]]
        self.circuit.set_gates(gates, gate_indicies)
        self.circuit.apply_all_gates()
        Qubit.display_all_qubits()

        time.sleep(2)
        results = self.circuit.measure_all()

        Qubit.display_all_qubits()
        print("Measurement results:", results)
