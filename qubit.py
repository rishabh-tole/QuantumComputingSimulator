import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from abc import ABC, abstractmethod

# Qubit Class
class Qubit:
    all_qubit_figures = []

    def __init__(self, a = 1, b = 0):
        self.alpha = a  # Start in |0⟩ state
        self.beta = b
        self.normalize()
        self.fig = self.create_qubit_figure()
        Qubit.all_qubit_figures.append(self.fig)

    def set_state(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.normalize()
        self.fig = self.create_qubit_figure()

    def get_state(self):
        return np.array([self.alpha, self.beta], dtype=np.complex128)

    def measure(self):
        prob_zero = abs(self.alpha) ** 2
        if np.random.random() < prob_zero:
            self.set_state(1, 0)
            return 0
        else:
            self.set_state(0, 1)
            return 1

    def normalize(self):
        magnitude = np.sqrt(abs(self.alpha) ** 2 + abs(self.beta) ** 2)
        self.alpha /= magnitude
        self.beta /= magnitude

    def create_qubit_figure(self):
        theta = 2 * math.acos(abs(self.alpha))
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
            marker=dict(size=4),
            line=dict(color='red', width=5)
        ))

        return fig

    def __str__(self):
        return f"Qubit state vector: |ψ> = {self.alpha} |0⟩ + {self.beta} |1⟩"

