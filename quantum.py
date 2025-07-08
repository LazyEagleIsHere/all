from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import math
import time

backend = AerSimulator()
max_qubits = backend.configuration().n_qubits

def batch_quantum_bits(num_bits, num_rolls):
  total_qubits = num_bits * num_rolls
  qc = QuantumCircuit(total_qubits, total_qubits)
  qc.h(range(total_qubits))
  qc.measure(range(total_qubits), range(total_qubits))

  compiled_circuit = transpile(qc, backend, optimization_level=3)
  job = backend.run(compiled_circuit, shots=1)
  result = job.result()
  counts = result.get_counts()

  bitstring = list(counts.keys())[0]
  bitstring = bitstring[::-1]

  rolls_bits = [bitstring[i*num_bits:(i+1)*num_bits] for i in range(num_rolls)]
  rolls = [int(bits, 2) for bits in rolls_bits]
  return rolls

def quantum_random_numbers(max_value, num_rolls):
  num_bits = math.ceil(math.log2(max_value))
  results = []
  max_rolls_per_batch = max_qubits // num_bits

  while len(results) < num_rolls:
    batch_size = min(max_rolls_per_batch, num_rolls - len(results))
    batch = batch_quantum_bits(num_bits, batch_size)
    batch_filtered = [n for n in batch if 1 <= n <= max_value]
    results.extend(batch_filtered)

  return results[:num_rolls]

def roll_quantum_dice(sides=6, num_rolls=10):
  return quantum_random_numbers(sides, num_rolls)[0]

# start = time.time()
# results = roll_quantum_dice(sides=6, num_rolls=5)
# end = time.time()

# print("Quantum dice rolls:", results)
# print(f"Execution time: {end - start:.4f} seconds")
