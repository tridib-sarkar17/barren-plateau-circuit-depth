from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

def build_param_circuit(num_qubits=2, depth=2, name='theta'):
    """
    Build a parameterized quantum circuit with given depth.
    
    Args:
        num_qubits (int): Number of qubits (default 2).
        depth (int): Number of layers (rotations + entanglement).
        name (str): Name prefix for parameters.
    
    Returns:
        QuantumCircuit, ParameterVector
    """
    # Each layer needs 2 parameters per qubit (here only RY rotations per qubit)
    params = ParameterVector(name, num_qubits * depth)
    qc = QuantumCircuit(num_qubits)

    for i in range(depth):
        # Apply rotations on each qubit
        for q in range(num_qubits):
            qc.ry(params[i*num_qubits + q], q)
        # Add entanglement (CX between qubit 0 and 1)
        qc.cx(0, 1)

    return qc, params

# Example usage:
qc_shallow, params_shallow = build_param_circuit(num_qubits=2, depth=2, name='theta')
qc_deep, params_deep = build_param_circuit(num_qubits=2, depth=6, name='phi')

print("Shallow Circuit:")
print(qc_shallow)

print("\nDeep Circuit:")
print(qc_deep)

# Visualize (works in Jupyter/Colab, not plain CMD)
qc_shallow.draw('mpl')
qc_deep.draw('mpl')
