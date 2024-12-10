
import numpy as np
from abc import ABC, abstractmethod
from qubit import Qubit
from entangled_qubit import EntangledQubit

class Gate(ABC):
    @abstractmethod
    def get_matrix(self):
        pass

    def apply(self, target, target_indices=None):
        if isinstance(target, Qubit):
            # Apply gate to a single qubit
            state = target.get_state()
            result = self.get_matrix() @ state
            target.set_state(result[0], result[1])
        elif isinstance(target, EntangledQubit):
            # Apply gate to an entangled state
            if target_indices is None:
                raise ValueError("Target indices must be specified for entangled qubits.")
            target.apply_gate(self.get_matrix(), target_indices)



# Specific Gates
class CNOTGate(Gate):
    def get_matrix(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])


class HadamardGate:
    def apply(self, target, target_indices=None):
        """Apply the Hadamard gate to the target qubit."""
        # Check if the input is a single qubit
        if not isinstance(target, Qubit):
            raise ValueError("HadamardGate can only be applied to a single qubit.")

        # Define the Hadamard transformation matrix
        hadamard_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        # Update the qubit's state
        target.state = np.dot(hadamard_matrix, target.state)


class PauliXGate(Gate):
    def get_matrix(self):
        return np.array([
            [0, 1],
            [1, 0]
        ])
    
class PauliYGate(Gate):
    def get_matrix(self):
        return np.array([
            [0, -1j],  
            [1j, 0]    
        ])

class PauliZGate(Gate):
    def get_matrix(self):
        return np.array([
            [1, 0],    
            [0, -1] 
        ])