import math

class Complex:
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def add(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def subtract(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def multiply(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return Complex(real, imag)

    def divide(self, other):
        denom = other.real**2 + other.imag**2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return Complex(real, imag)

    def magnitude(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def __repr__(self):
        return f"{self.real} + {self.imag}i"
