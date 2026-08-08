import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Pauli, Statevector

# --- Cost function ---
def cost_function(circuit, params, target=0):
    # Assign parameters instead of bind_parameters
    bound_circuit = circuit.assign_parameters(params)
    sv = Statevector.from_instruction(bound_circuit)
    observable = Pauli('Z' * circuit.num_qubits)
    exp_val = sv.expectation_value(observable)
    return (exp_val.real - target)**2

# --- Training function (finite-difference gradient) ---
def train(circuit, num_params, iterations=20, lr=0.1):
    losses = []
    grads = []
    theta = np.random.uniform(-np.pi, np.pi, num_params)

    for i in range(iterations):
        # Compute loss
        loss = cost_function(circuit, theta)
        losses.append(loss)

        # Approximate gradient
        grad = []
        eps = 1e-3
        for j in range(num_params):
            theta_plus = theta.copy()
            theta_minus = theta.copy()
            theta_plus[j] += eps
            theta_minus[j] -= eps
            grad_val = (cost_function(circuit, theta_plus) - cost_function(circuit, theta_minus)) / (2 * eps)
            grad.append(grad_val)
        grad = np.array(grad)

        grad_mag = np.linalg.norm(grad)
        grads.append(grad_mag)

        # Gradient descent update
        theta = theta - lr * grad

    return losses, grads

# --- Build shallow circuit (2 layers) ---
params_shallow = ParameterVector('theta', 4)
qc_shallow = QuantumCircuit(2)
qc_shallow.ry(params_shallow[0], 0)
qc_shallow.ry(params_shallow[1], 1)
qc_shallow.cx(0, 1)
qc_shallow.ry(params_shallow[2], 0)
qc_shallow.ry(params_shallow[3], 1)
qc_shallow.cx(0, 1)

# --- Build deep circuit (6 layers) ---
params_deep = ParameterVector('phi', 12)
qc_deep = QuantumCircuit(2)
for i in range(6):
    qc_deep.ry(params_deep[2*i], 0)
    qc_deep.ry(params_deep[2*i+1], 1)
    qc_deep.cx(0, 1)

# --- Train both ---
shallow_losses, shallow_grads = train(qc_shallow, len(params_shallow))
deep_losses, deep_grads = train(qc_deep, len(params_deep))

print("Shallow losses:", shallow_losses)
print("Shallow gradients:", shallow_grads)
print("Deep losses:", deep_losses)
print("Deep gradients:", deep_grads)

#plotting code begins 
import matplotlib.pyplot as plt

# Plot Loss vs Iterations
plt.figure(figsize=(8,5))
plt.plot(shallow_losses, label="Shallow Circuit Loss", marker='o')
plt.plot(deep_losses, label="Deep Circuit Loss", marker='x')
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.title("Loss vs Iterations")
plt.legend()
plt.savefig("loss_plot.png")
plt.show()

# Plot Gradient Magnitudes vs Iterations
plt.figure(figsize=(8,5))
plt.plot(shallow_grads, label="Shallow Circuit Gradients", marker='o')
plt.plot(deep_grads, label="Deep Circuit Gradients", marker='x')
plt.xlabel("Iteration")
plt.ylabel("Gradient Magnitude")
plt.title("Gradient Magnitudes vs Iterations")
plt.legend()
plt.savefig("gradients_plot.png")
plt.show()

