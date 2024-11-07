import numpy as np

class Matrix:
    def __init__(self, elements):
        self.elements = np.array(elements)

    def multiply(self, other):
        return Matrix(np.dot(self.elements, other.elements))

    def tensor_product(self, other):
        return Matrix(np.kron(self.elements, other.elements))

    def apply_to_vector(self, vector):
        return np.dot(self.elements, vector)

    def get_transpose(self):
        return Matrix(self.elements.T)
