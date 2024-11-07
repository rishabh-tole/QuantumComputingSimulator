import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from complex import Complex  # Assuming Complex is your custom class for complex operations

class Qubit:
    all_qubit_figures = []
    qubit_indices = []  # List to store the indices of each qubit's figure

    def __init__(self):
        self.alpha = Complex(1, 0)  # Start in |0⟩ state
        self.beta = Complex(0, 0)
        self.normalize()
        self.fig = self.create_qubit_figure()  # Initialize the figure for this qubit
        self.index = len(Qubit.all_qubit_figures)  # Store the index for this qubit
        Qubit.all_qubit_figures.append(self.fig)  # Append the figure to the class-wide list
        Qubit.qubit_indices.append(self.index)  # Store the index in the list

    def set_state(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.normalize()
        self.fig = self.create_qubit_figure()  # Update this qubit's figure
        # Update the figure in the list using its index
        Qubit.all_qubit_figures[self.index] = self.fig
        return self

    def get_state(self):
        alpha_complex = complex(self.alpha.real, self.alpha.imag)
        beta_complex = complex(self.beta.real, self.beta.imag)
        return np.array([alpha_complex, beta_complex], dtype=np.complex128)

    def measure(self):
        prob_zero = self.alpha.magnitude() ** 2
        if np.random.random() < prob_zero:
            self.set_state(Complex(1, 0), Complex(0, 0))
            return 0
        else:
            self.set_state(Complex(0, 0), Complex(1, 0))
            return 1

    def normalize(self):
        mag = math.sqrt(self.alpha.magnitude()**2 + self.beta.magnitude()**2)
        self.alpha = Complex(self.alpha.real / mag, self.alpha.imag / mag)
        self.beta = Complex(self.beta.real / mag, self.beta.imag / mag)

    def __str__(self):
        return f"Qubit state vector: [{self.alpha.real} + {self.alpha.imag}i, {self.beta.real} + {self.beta.imag}i]"

    def create_qubit_figure(self):
        theta = 2 * math.acos(self.alpha.magnitude())
        phi = math.atan2(self.beta.imag, self.beta.real)

        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)

        fig = go.Figure()

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        fig.add_trace(go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.1, colorscale='Blues'))

        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            marker=dict(size=2),
            line=dict(color='red', width=5)
        ))

        return fig

    @staticmethod
    def display_all_qubits():
        num_qubits = len(Qubit.all_qubit_figures)
        num_columns = 3
        num_rows = math.ceil(num_qubits / num_columns)

        fig = make_subplots(
            rows=num_rows, cols=num_columns,
            specs=[[{'type': 'surface'} for _ in range(num_columns)] for _ in range(num_rows)],
            subplot_titles=[f"Qubit {i + 1}" for i in range(num_qubits)]
        )

        # Add each qubit figure to the subplot
        for i, qubit_fig in enumerate(Qubit.all_qubit_figures):
            row = (i // num_columns) + 1
            col = (i % num_columns) + 1
            for trace in qubit_fig.data:
                fig.add_trace(trace, row=row, col=col)

        fig.update_layout(
            title="All Qubits",
            width=900,
            height=300 * num_rows,
            showlegend=False,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        fig.show()