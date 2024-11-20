import numpy as np

class QuantumState:
    def __init__(self, qubits):
        self.qubits = qubits
        self.num_qubits = len(qubits)
        self.state_vector = self.get_combined_state_vector()

    def apply_gate(self, gate_matrix, qubit_indices):
        num_gate_qubits = len(qubit_indices)

        # Expand the gate matrix to the full system size
        if num_gate_qubits == 1:
            full_matrix = self.expand_single_qubit_gate(gate_matrix, qubit_indices[0])
        else:
            full_matrix = self.expand_multi_qubit_gate(gate_matrix, qubit_indices)

        # Apply the gate to the state vector
        self.state_vector = full_matrix @ self.state_vector

        # Update individual qubits based on the new state vector
        self.set_combined_state_vector(self.state_vector)

    def expand_single_qubit_gate(self, gate_matrix, target_qubit):
        """Expands a single-qubit gate matrix to operate on the full system."""
        full_matrix = np.eye(1)
        for i in range(self.num_qubits):
            if i == target_qubit:
                full_matrix = np.kron(full_matrix, gate_matrix)
            else:
                full_matrix = np.kron(full_matrix, np.eye(2))
        return full_matrix

    def expand_multi_qubit_gate(self, gate_matrix, qubit_indices):
        """Expands a multi-qubit gate matrix to operate on the full system."""
        num_gate_qubits = len(qubit_indices)
        gate_size = 2 ** num_gate_qubits

        if gate_matrix.shape != (gate_size, gate_size):
            raise ValueError("Gate matrix size does not match the number of qubits.")

        # Create a full identity matrix for all qubits
        identity_size = 2 ** self.num_qubits
        full_matrix = np.eye(identity_size, dtype=complex)

        # Calculate the indices for the qubits being targeted
        for i in range(identity_size):
            binary = f"{i:0{self.num_qubits}b}"
            if all(binary[idx] == '1' for idx in qubit_indices):
                full_matrix[i, i] = gate_matrix[i % gate_size, i % gate_size]
        return full_matrix

    def get_combined_state_vector(self):
        """Combines all qubit states into a single state vector."""
        combined_state = self.qubits[0].get_state()
        for qubit in self.qubits[1:]:
            combined_state = np.kron(combined_state, qubit.get_state())
        return combined_state

    def set_combined_state_vector(self, combined_state):
        """Sets the state vector for the entire system."""
        self.state_vector = combined_state

        # Update individual qubits
        state_splits = np.split(combined_state, len(self.qubits))
        for i, qubit in enumerate(self.qubits):
            alpha, beta = state_splits[i]
            qubit.set_state(alpha, beta)
