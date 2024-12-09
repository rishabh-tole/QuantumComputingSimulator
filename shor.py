from quantum_simulator import QuantumSimulator
from quantum_circuit import QuantumCircuit
from qubit import Qubit
from entangled_qubit import EntangledQubit
from gate import HadamardGate, PauliXGate, PauliZGate
import numpy as np
from math import gcd, ceil, log2

class ControlledUGate(PauliXGate):
    def __init__(self, base, power, mod):
        """
        Controlled-U gate for modular exponentiation.
        Args:
            base: The base of the modular exponentiation (a in a^x mod N).
            power: The power to which the base is raised.
            mod: The modulus N.
        """
        self.base = base
        self.power = power
        self.mod = mod

    def get_matrix(self):
        """
        Generate the matrix representation of the controlled-U operation.
        Each matrix element corresponds to modular exponentiation of the form (a^x mod N).
        """
        size = 4  # For two-qubit entangled states
        matrix = np.identity(size, dtype=np.complex128)
        for i in range(size):
            matrix[i][i] = modular_exponentiation(self.base, self.power, self.mod) % self.mod
        return matrix

class ShorsAlgorithm:
    def __init__(self, N):
        """
        Initialize the Shor's algorithm instance.
        Args:
            N: The number to factor.
        """
        self.N = N  # Number to factor
        self.a = None  # Random co-prime for modular exponentiation
        self.circuit = QuantumCircuit()  # Quantum circuit for simulation
        self.entangled_register = None  # Register of entangled qubits

    def classical_modular_exponentiation(self, base, exponent, mod):
        """
        Efficient classical modular exponentiation: (base^exponent) % mod.
        """
        result = 1
        base = base % mod
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % mod
            exponent //= 2
            base = (base * base) % mod
        return result

    def modular_exponentiation(self):
        """
        Simulate modular exponentiation on entangled qubits.
        Each qubit controls a modular multiplication operation with increasing powers.
        """
        for control_qubit in range(len(self.entangled_register.qubits)):
            power = 2 ** control_qubit  # 2^control_qubit determines the power of the base
            gate = ControlledUGate(self.a, power, self.N)
            self.circuit.add_gate(gate, [control_qubit])  # Add controlled gate to the circuit

    def inverse_qft(self):
        """
        Implement the inverse Quantum Fourier Transform (QFT).
        This converts the entangled state into one that encodes the periodicity of the function.
        """
        num_qubits = len(self.entangled_register.qubits)
        for qubit in reversed(range(num_qubits)):
            self.circuit.add_gate(HadamardGate(), [qubit])  # Apply Hadamard gate
            for target_qubit in reversed(range(qubit)):
                angle = -np.pi / (2 ** (qubit - target_qubit))  # Controlled phase rotation
                self.circuit.add_gate(self.create_controlled_rotation(angle), [target_qubit, qubit])

    def create_controlled_rotation(self, angle):
        """
        Create a controlled rotation gate.
        Args:
            angle: The angle of rotation for the gate.
        Returns:
            ControlledRotationGate: A custom gate for controlled rotations.
        """
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
        """
        Quantum subroutine to find the period of the modular exponentiation function.
        Returns:
            The period (r) of the function a^x mod N.
        """
        # Determine the number of qubits needed
        num_qubits = 2 * ceil(log2(self.N))  # Sufficient resolution for the periodicity

        # Create entangled qubits with appropriate size
        self.entangled_register = EntangledQubit([Qubit(1, 0) for _ in range(num_qubits)])
        self.circuit.add_qubit(self.entangled_register)

        # Apply Hadamard gates to all qubits to create superposition
        for idx, qubit in enumerate(self.entangled_register.qubits):
            self.circuit.add_gate(HadamardGate(), [idx])

        # Apply modular exponentiation
        self.modular_exponentiation()

        # Apply inverse QFT to decode periodicity
        self.inverse_qft()

        # Measure all qubits and extract the result
        measurements = self.circuit.measure_all()
        return self.measurement_to_period(measurements)

    def measurement_to_period(self, measurements):
        """
        Convert quantum measurements into an integer period.
        Args:
            measurements: The measured quantum state (as binary strings).
        Returns:
            The period as an integer.
        """
        binary_string = ''.join(reversed(measurements))  # Convert measurements to a binary string
        measured_value = int(binary_string, 2)  # Convert binary string to an integer
        return measured_value

    def run(self):
        """
        Main algorithm for factoring N.
        Returns:
            A tuple of two factors of N or a failure message.
        """
        # Handle even numbers directly
        if self.N % 2 == 0:
            return 2, self.N // 2

        # Attempt to find factors via the quantum period-finding routine
        for attempt in range(5):  # Retry a few times for robustness
            self.a = np.random.randint(2, self.N - 1)  # Random co-prime
            if gcd(self.a, self.N) > 1:
                return gcd(self.a, self.N), self.N // gcd(self.a, self.N)

            print(f"Attempt {attempt + 1}: Trying a = {self.a}")
            period = self.find_period()  # Quantum subroutine to find the period
            if not period or period % 2 != 0:
                continue  # Retry if no valid period is found

            # Use the period to compute factors
            x = self.classical_modular_exponentiation(self.a, period // 2, self.N)
            if x == 1 or x == self.N - 1:
                continue  # Retry if period leads to trivial factors

            factor1 = gcd(x - 1, self.N)
            factor2 = gcd(x + 1, self.N)

            if factor1 * factor2 == self.N and factor1 > 1 and factor2 > 1:
                return factor1, factor2

        return "Failed to find factors"

# Main entry point
if __name__ == "__main__":
    number_to_factor = 31*11  # Example: A large number to factor
    print(f"Factoring {number_to_factor} using Shor's Algorithm...")
    shor = ShorsAlgorithm(number_to_factor)
    factors = shor.run()
    print(f"Factors of {number_to_factor}: {factors}")
