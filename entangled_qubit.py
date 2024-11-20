import numpy as np
from qubit import Qubit

class EntangledQubit:
    def __init__(self, qubits):
        if len(qubits) < 2:
            raise ValueError("EntangledQubit requires at least 2 qubits.")
        self.qubits = qubits
        self.num_qubits = len(qubits)
        self.state_vector = np.zeros(2 ** self.num_qubits, dtype=np.complex128)

        # Create an entangled state: (|00...0⟩ + |11...1⟩) / sqrt(2)
        self.state_vector[0] = 1 / np.sqrt(2)  # Coefficient of |00...0⟩
        self.state_vector[-1] = 1 / np.sqrt(2)  # Coefficient of |11...1⟩

    def get_state(self):
        """Return the full state vector of the entangled qubit."""
        return self.state_vector

    def measure(self):
        probabilities = np.abs(self.state_vector) ** 2
        result = np.random.choice(len(probabilities), p=probabilities)

        # Collapse the state
        new_state_vector = np.zeros_like(self.state_vector)
        new_state_vector[result] = 1
        self.state_vector = new_state_vector

        # Map result to binary representation
        result_binary = f"{result:0{self.num_qubits}b}"
        return result_binary

    def __str__(self):
        state_description = "Entangled Qubit State Vector:\n"
        for i, amplitude in enumerate(self.state_vector):
            binary_state = f"|{i:0{self.num_qubits}b}>"
            state_description += f" {amplitude:.3f} {binary_state}\n"
        return state_description
