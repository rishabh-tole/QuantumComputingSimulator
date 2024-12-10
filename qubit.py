import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Qubit Class
class Qubit:
    all_qubit_figures = []

    def __init__(self, a=1, b=0):
        """Initialize a qubit in a state |ψ> = a|0⟩ + b|1⟩."""
        self.alpha = a  # Amplitude of |0⟩
        self.beta = b   # Amplitude of |1⟩
        self.normalize()  # Ensure the state is normalized
        self.fig = self.create_qubit_figure()
        Qubit.all_qubit_figures.append(self.fig)

    @property
    def state(self):
        """Get the state vector as [alpha, beta]."""
        return np.array([self.alpha, self.beta], dtype=np.complex128)

    @state.setter
    def state(self, new_state):
        """Set the state vector and normalize it."""
        if len(new_state) != 2:
            raise ValueError("State vector must have exactly two components.")
        self.alpha, self.beta = new_state
        self.normalize()

    def set_state(self, alpha, beta):
        """Set the state using separate alpha and beta values."""
        self.alpha = alpha
        self.beta = beta
        self.normalize()
        self.fig = self.create_qubit_figure()

    def get_state(self):
        """Get the state vector (deprecated, use .state property instead)."""
        return self.state

    def measure(self):
        """Perform a measurement on the qubit, collapsing it to |0⟩ or |1⟩."""
        prob_zero = abs(self.alpha) ** 2
        if np.random.random() < prob_zero:
            self.set_state(1, 0)  # Collapse to |0⟩
            return 0
        else:
            self.set_state(0, 1)  # Collapse to |1⟩
            return 1

    def normalize(self):
        """Normalize the state vector to ensure |ψ|^2 = 1."""
        magnitude = np.sqrt(abs(self.alpha) ** 2 + abs(self.beta) ** 2)
        self.alpha /= magnitude
        self.beta /= magnitude

    def create_qubit_figure(self):
        """Create a 3D Bloch sphere representation of the qubit."""
        theta = 2 * math.acos(abs(self.alpha))  # Polar angle
        phi = math.atan2(self.beta.imag, self.beta.real)  # Azimuthal angle

        # Cartesian coordinates for the Bloch vector
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)

        # Plot Bloch sphere
        fig = go.Figure()

        # Create the sphere surface
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        fig.add_trace(go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.1, colorscale='Blues'))

        # Add the Bloch vector
        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            marker=dict(size=4),
            line=dict(color='red', width=5)
        ))

        return fig

    def __str__(self):
        """String representation of the qubit's state vector."""
        return f"Qubit state vector: |ψ> = {self.alpha} |0⟩ + {self.beta} |1⟩"
