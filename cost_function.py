from qiskit_aer import Aer
from qiskit import transpile
from qiskit.quantum_info import Pauli, Statevector

# Backend simulator
backend = Aer.get_backend('statevector_simulator')

# Define cost function
def cost_function(circuit, params, target=0):
    # Bind parameters to circuit
    bound_circuit = circuit.bind_parameters(params)

    # Run simulation
    sv = Statevector.from_instruction(bound_circuit)

    # Define observable (Z on last qubit)
    observable = Pauli('Z' * circuit.num_qubits)

    # Expectation value
    exp_val = sv.expectation_value(observable)

    # Cost = squared difference from target
    return (exp_val.real - target)**2
