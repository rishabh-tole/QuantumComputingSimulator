
from shor import ShorsAlgorithm


number_to_factor = 4213*4241  # Example number to factor
print(f"Factoring {number_to_factor} using Shor's Algorithm...")
shor = ShorsAlgorithm(number_to_factor)
factors = shor.run()
print(f"Factors of {number_to_factor}: {factors}")