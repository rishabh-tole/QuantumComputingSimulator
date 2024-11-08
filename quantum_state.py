import numpy as np
from complex import Complex

class QuantumState:
    def __init__(self, qubits):
        self.qubits = qubits

    def apply_gate(self, gate_matrix, qubit_indices):
        # Loop through each qubit index in the list of qubits to apply the gate
        for idx in qubit_indices:
            # Get the qubit's state vector
            state_vector = self.qubits[idx].get_state()
            
            # Apply the gate matrix to the state vector (assuming gate_matrix is a matrix that works on a 2x1 vector)
            new_state = gate_matrix.apply_to_vector(state_vector)
            
            # Assume new_state is a 2x1 array or list containing [new_alpha, new_beta]
            new_alpha = new_state[0]
            new_beta = new_state[1]
            
            # Update the qubit's state using set_state, passing the new Complex values
            self.qubits[idx].set_state(Complex(new_alpha.real, new_alpha.imag), Complex(new_beta.real, new_beta.imag))


    def measure(self):
        return [qubit.measure() for qubit in self.qubits]

    def normalize(self):
        norm = np.linalg.norm(self.state_vector)
        self.state_vector = self.state_vector / norm
