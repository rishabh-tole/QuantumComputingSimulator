from quantum_simulator import QuantumSimulator
from quantum_circuit import QuantumCircuit
from qubit import Qubit
from entangled_qubit import EntangledQubit
from gate import HadamardGate, PauliXGate, PauliZGate
import numpy as np
from math import gcd, ceil, log2

def modular_exponentiation(base, exponent, mod):
    """Efficient modular exponentiation: (base^exponent) % mod."""
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent //= 2
        base = (base * base) % mod
    return result


class ControlledUGate(PauliXGate):
    def __init__(self, base, power, mod):
        self.base = base
        self.power = power
        self.mod = mod

    def get_matrix(self):
        """Generate a controlled-U matrix."""
        # Identity for no-operation paths
        identity = np.eye(2, dtype=np.complex128)
        # Target operation when control qubit is |1⟩
        target = np.array([
            [1, 0],
            [0, modular_exponentiation(self.base, self.power, self.mod) % self.mod]
        ], dtype=np.complex128)
        # Controlled-U matrix in 4x4 space
        return np.block([
            [identity, np.zeros_like(identity)],
            [np.zeros_like(identity), target]
        ])
    
    def apply(self, targets, target_indices=None):
        """Apply the controlled-U gate."""
        if len(targets) != 2:
            raise ValueError(f"Expected 2 qubits (control and target), got {len(targets)}")
        print(f"Control Qubit: {targets[0]}, Target Qubit: {targets[1]}")

        control, target = targets
        if control.measure() == 1:
            u_matrix = self.get_matrix()
            # Apply the matrix on the full two-qubit system (control and target)
            combined_state = np.kron(control.state, target.state)  # Tensor product of control and target states
            new_state = np.dot(u_matrix, combined_state)
            
            # Split the new state back into control and target qubits
            control.state = new_state[:2]  # First half of the new state
            target.state = new_state[2:]   # Second half of the new state

class ShorsAlgorithm:
    def __init__(self, N):
        """Initialize the Shor's algorithm instance."""
        self.N = N  # Number to factor
        self.a = None  # Random co-prime for modular exponentiation
        self.circuit = QuantumCircuit()  # Quantum circuit for simulation
        self.entangled_register = None  # Register of entangled qubits

    def classical_modular_exponentiation(self, base, exponent, mod):
        """Efficient classical modular exponentiation: (base^exponent) % mod."""
        result = 1
        base = base % mod
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % mod
            exponent //= 2
            base = (base * base) % mod
        return result

    def log_state_vector(self, label):
        """Display the current state vector of the quantum system."""
          # Ensure gates are applied before logging
        print(f"\nState Vector after {label}:")
        for idx, qubit in enumerate(self.entangled_register.qubits):
            print(f"Qubit {idx}: {qubit.get_state()}")

    def modular_exponentiation(self):
        """Implement modular exponentiation on entangled qubits."""
        num_qubits = len(self.entangled_register.qubits)
        for control_qubit in range(num_qubits):
            power = 2 ** control_qubit
            gate = ControlledUGate(self.a, power, self.N)

            # Ensure target_qubit is within bounds
            target_qubit = (control_qubit + 1) % num_qubits  # Wrap around if needed
            if target_qubit >= num_qubits:
                raise IndexError(f"Target qubit index {target_qubit} out of range for control qubit {control_qubit}")

            self.circuit.add_gate(gate, [control_qubit, target_qubit])  # Add controlled gate
        self.circuit.apply_all_gates()  # Apply gates



    def inverse_qft(self):
        """Implement the inverse Quantum Fourier Transform (QFT)."""
        num_qubits = len(self.entangled_register.qubits)
        for qubit in reversed(range(num_qubits)):
            self.circuit.add_gate(HadamardGate(), [qubit])  # Apply Hadamard gate
            for target_qubit in reversed(range(qubit)):
                angle = -np.pi / (2 ** (qubit - target_qubit))  # Controlled phase rotation
                self.circuit.add_gate(self.create_controlled_rotation(angle), [target_qubit, qubit])
        self.circuit.apply_all_gates()  # Ensure gates are applied

    def create_controlled_rotation(self, angle):
        """Create a controlled rotation gate."""
        class ControlledRotationGate(PauliZGate):
            def __init__(self, angle):
                self.angle = angle

            def get_matrix(self):
                return np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, np.exp(1j * self.angle)]
                ])
        return ControlledRotationGate(angle)

    def find_period(self):
        self.circuit = QuantumCircuit()  # Reset the quantum circuit

        # Determine the number of qubits needed
        num_qubits = 2 * ceil(log2(self.N))
        self.entangled_register = EntangledQubit([Qubit(1, 0) for _ in range(num_qubits)])
        for qubit in self.entangled_register.qubits:
            self.circuit.add_qubit(qubit)  # Add each qubit to the circuit

        self.log_state_vector("Initializing Entangled Register")

        # Apply Hadamard gates to all qubits
        for idx in range(len(self.entangled_register.qubits)):
            self.circuit.add_gate(HadamardGate(), [idx])
            
        self.circuit.apply_all_gates()  # Apply all gates
        self.log_state_vector("Applying Hadamard Gates")

        # Apply modular exponentiation
        self.modular_exponentiation()
        self.log_state_vector("Modular Exponentiation")

        # Apply inverse QFT
        self.inverse_qft()
        
        # Measure all qubits
        measurements = self.circuit.measure_all()
        return self.measurement_to_period(measurements)

    def measurement_to_period(self, measurements):
        """Convert quantum measurements into an integer period."""
        binary_string = ''.join(str(measurement) for measurement in reversed(measurements))  # Convert measurements to a binary string
        measured_value = int(binary_string, 2)  # Convert binary string to an integer
        return measured_value


    def run(self):
        """Main algorithm for factoring N."""
        if self.N % 2 == 0:
            return 2, self.N // 2

        for attempt in range(30):  # Retry a few times for robustness
            self.a = np.random.randint(2, self.N - 1)
            if gcd(self.a, self.N) > 1:
                return gcd(self.a, self.N), self.N // gcd(self.a, self.N)

            print(f"Attempt {attempt + 1}: Trying a = {self.a}")
            period = self.find_period()
            if not period or period % 2 != 0:
                continue

            x = self.classical_modular_exponentiation(self.a, period // 2, self.N)
            if x == 1 or x == self.N - 1:
                continue

            factor1 = gcd(x - 1, self.N)
            factor2 = gcd(x + 1, self.N)

            if factor1 * factor2 == self.N and factor1 > 1 and factor2 > 1:
                return factor1, factor2

        return "Failed to find factors"

# Main entry point
if __name__ == "__main__":

    number_to_factor = 77  # Example number to factor
    print(f"Factoring {number_to_factor} using Shor's Algorithm...")
    shor = ShorsAlgorithm(number_to_factor)
    factors = shor.run()
    print(f"Factors of {number_to_factor}: {factors}")
