class QuantumCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def add_qubit(self, qubit):
        self.qubits.append(qubit)

    def add_gate(self, gate, target_indices):
        self.gates.append((gate, target_indices))


    def apply_all_gates(self):
        print("\n--- Applying Gates ---")
        for gate, indices in self.gates:
            if len(indices) == 1:  # Single-qubit gate
                target = self.qubits[indices[0]]
                print(f"Applying {gate.__class__.__name__} to Qubit {indices[0]}")
                gate.apply(target, target_indices=[indices[0]])
            else:  # Multi-qubit gate
                targets = [self.qubits[i] for i in indices]
                print(f"Applying {gate.__class__.__name__} to Qubits {indices}")
                # For multi-qubit gates, pass all indices
                gate.apply(targets[0], target_indices=indices)

    def measure_all(self):
        results = []
        print("\n--- Measuring All Qubits ---")
        for idx, qubit in enumerate(self.qubits):
            result = qubit.measure()
            print(f"Measurement result for Qubit {idx}: {result}")
            results.append(result)
        return results
