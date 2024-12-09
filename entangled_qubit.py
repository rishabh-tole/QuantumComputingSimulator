import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from abc import ABC, abstractmethod

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

    def apply_gate(self, gate_matrix, target_indices):
        """
        Applies a gate to the entangled state vector.
        """
        full_gate = self.expand_gate(gate_matrix, target_indices)
        self.state_vector = full_gate @ self.state_vector

    def expand_gate(self, gate_matrix, target_indices):
        """
        Dynamically expands a gate matrix to operate on the entangled state.
        """
        num_total_qubits = self.num_qubits
        identity = np.eye(1)
        for i in range(num_total_qubits):
            if i in target_indices:
                identity = np.kron(identity, gate_matrix)
            else:
                identity = np.kron(identity, np.eye(2))
        return identity

    def measure(self):
        probabilities = np.abs(self.state_vector) ** 2
        result = np.random.choice(len(probabilities), p=probabilities)

        new_state_vector = np.zeros_like(self.state_vector)
        new_state_vector[result] = 1
        self.state_vector = new_state_vector

        result_binary = f"{result:0{self.num_qubits}b}"
        return result_binary

    def display_entangled_state(self):
        fig = go.Figure()

        # Add bars for each state in the entangled superposition
        for i, amplitude in enumerate(self.state_vector):
            binary_state = f"|{i:0{self.num_qubits}b}>"
            fig.add_trace(go.Bar(
                x=[binary_state],
                y=[abs(amplitude) ** 2],
                name=binary_state
            ))

        fig.update_layout(
            title="Entangled Qubit State Probabilities",
            xaxis_title="Quantum States",
            yaxis_title="Probability",
            showlegend=False
        )

        fig.show()

    def __str__(self):
        state_description = "Entangled Qubit State Vector:\n"
        for i, amplitude in enumerate(self.state_vector):
            binary_state = f"|{i:0{self.num_qubits}b}>"
            state_description += f" {amplitude:.3f} {binary_state}\n"
        return state_description
