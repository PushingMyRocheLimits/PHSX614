#===== I.2.1 =====
def my_circuit(theta, phi):
    ##################
    # YOUR CODE HERE #
    ##################

    # REORDER THESE 5 GATES TO MATCH THE CIRCUIT IN THE PICTURE

    qp.CNOT(wires=[0, 1])
    qp.RX(theta, wires=2)
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[2, 0])
    qp.RY(phi, wires=1)

    # This is the measurement; we return the probabilities of all possible output states
    # You'll learn more about what types of measurements are available in a later node
    return qp.probs(wires=[0, 1, 2])

#===== I.2.2 ======
# This creates a device with three wires on which PennyLane can run computations
dev = qp.device("default.qubit", wires=3)


def my_circuit(theta, phi, omega):

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE CIRCUIT BY ADDING THE GATES

    # Here are two examples, so you can see the format:
    # qp.CNOT(wires=[0, 1])
    # qp.RX(theta, wires=0)
    qp.RX(theta, wires = 0)
    qp.RY(phi, wires = 1)
    qp.RZ(omega, wires = 2)
    qp.CNOT(wires = [0,1])
    qp.CNOT(wires = [1,2])
    qp.CNOT(wires = [2,0])
    

    return qp.probs(wires=[0, 1, 2])


# This creates a QNode, binding the function and device
my_qnode = qp.QNode(my_circuit, dev)

# We set up some values for the input parameters
theta, phi, omega = 0.1, 0.2, 0.3

# Now we can execute the QNode by calling it like we would a regular function
my_qnode(theta, phi, omega)

#===== I.2.3 ======
dev = qp.device("default.qubit", wires=3)

##################
# YOUR CODE HERE #
##################
@qp.qnode(dev)
# DECORATE THE FUNCTION BELOW TO TURN IT INTO A QNODE


def my_circuit(theta, phi, omega):
    qp.RX(theta, wires=0)
    qp.RY(phi, wires=1)
    qp.RZ(omega, wires=2)
    qp.CNOT(wires=[0, 1])
    qp.CNOT(wires=[1, 2])
    qp.CNOT(wires=[2, 0])
    return qp.probs(wires=[0, 1, 2])


theta, phi, omega = 0.1, 0.2, 0.3

##################
# YOUR CODE HERE #
##################
my_first_QNode = qp.QNode(my_circuit, dev)
# RUN THE QNODE WITH THE PROVIDED PARAMETERS

#===== I.2.4 ======
dev = qp.device("default.qubit", wires=3)


@qp.qnode(dev)
def my_circuit(theta, phi, omega):
    qp.RX(theta, wires=0)
    qp.RY(phi, wires=1)
    qp.RZ(omega, wires=2)
    qp.CNOT(wires=[0, 1])
    qp.CNOT(wires=[1, 2])
    qp.CNOT(wires=[2, 0])
    return qp.probs(wires=[0, 1, 2])


##################
# YOUR CODE HERE #
##################

# FILL IN THE CORRECT CIRCUIT DEPTH
depth = 4

#======================================================================================================================
#======================================================================================================================
# ===== I.3.1 =====
dev = qp.device("default.qubit", wires=1)

U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)


@qp.qnode(dev)
def apply_u():

    ##################
    # YOUR CODE HERE #
    ##################
    qp.QubitUnitary(U, wires=0)

    # USE QubitUnitary TO APPLY U TO THE QUBIT

    # Return the state
    return qp.state()
    
# ===== I.3.2 =====
dev = qp.device("default.qubit", wires=1)


@qp.qnode(dev)
def apply_u_as_rot(phi, theta, omega):

    ##################
    # YOUR CODE HERE #
    ##################

    # APPLY A ROT GATE USING THE PROVIDED INPUT PARAMETERS
    qp.Rot(phi, theta, omega, wires=0)
    # RETURN THE QUANTUM STATE VECTOR

    return qp.state()
#======================================================================================================================
#======================================================================================================================
# ===== I.4.1 =====
dev = qp.device("default.qubit", wires=1)

U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)


@qp.qnode(dev)
def varied_initial_state(state):
    """Complete the function such that we can apply the operation U to
    either |0> or |1> depending on the input argument flag.

    Args:
        state (int): Either 0 or 1. If 1, prepare the qubit in state |1>,
            otherwise, leave it in state 0.

    Returns:
        np.array[complex]: The state of the qubit after the operations.
    """
    ##################
    # YOUR CODE HERE #
    ##################
    if state == 1:
        qp.PauliX(wires=0)

    # APPLY U TO THE STATE
    qp.QubitUnitary(U, wires=0)

    return qp.state()
    
# ===== I.4.2 ======
dev = qp.device("default.qubit", wires=1)


@qp.qnode(dev)
def apply_hadamard():
    ##################
    # YOUR CODE HERE #
    ##################

    # APPLY THE HADAMARD GATE
    qp.Hadamard(wires=0)

    # RETURN THE STATE
    return qp.state()
    
# ===== I.4.3 ======
dev = qp.device("default.qubit", wires=1)


@qp.qnode(dev)
def apply_hadamard_to_state(state):
    """Complete the function such that we can apply the Hadamard to
    either |0> or |1> depending on the input argument flag.

    Args:
        state (int): Either 0 or 1. If 1, prepare the qubit in state |1>,
            otherwise, leave it in state 0.

    Returns:
        np.array[complex]: The state of the qubit after the operations.
    """
    ##################
    # YOUR CODE HERE #
    ##################

    # KEEP THE QUBIT IN |0> OR CHANGE IT TO |1> DEPENDING ON state
    if state == 1:
        qp.PauliX(wires=0)

    # APPLY THE HADAMARD
    qp.Hadamard(wires=0)

    # RETURN THE STATE

    return qp.state()


print(apply_hadamard_to_state(0))
print(apply_hadamard_to_state(1))

# ===== I.4.4 =====
##################
# YOUR CODE HERE #
##################
dev = qp.device("default.qubit", wires=1)
# CREATE A DEVICE
@qp.qnode(dev)
# CREATE A QNODE CALLED apply_hxh THAT APPLIES THE CIRCUIT ABOVE
def apply_hxh(state):
    if state == 1:
        qp.PauliX(wires=0)
    qp.Hadamard(wires=0)
    qp.PauliX(wires=0)
    qp.Hadamard(wires=0)
    return qp.state()

# Print your results
print(apply_hxh(0))
print(apply_hxh(1))

#======================================================================================================================
#======================================================================================================================
# ===== I.5.1 =====
dev = qp.device("default.qubit", wires=1)

@qp.qnode(dev)
def apply_z_to_plus():
    """Write a circuit that applies PauliZ to the |+> state and returns
    the state.

    Returns:
        np.array[complex]: The state of the qubit after the operations.
    """

    ##################
    # YOUR CODE HERE #
    ##################

    # CREATE THE |+> STATE
    qp.Hadamard(wires=0)

    # APPLY PAULI Z
    qp.PauliZ(wires=0)
    
    # RETURN THE STATE
    return qp.state()


print(apply_z_to_plus())

# ===== I.5.2 =====
dev = qp.device("default.qubit", wires=1)
@qp.qnode(dev)
def fake_z():
    """Use RZ to produce the same action as Pauli Z on the |+> state.

    Returns:
        np.array[complex]: The state of the qubit after the operations.
    """
    ##################
    # YOUR CODE HERE #
    ##################
    # CREATE THE |+> STATE
    qp.Hadamard(wires=0)

    # APPLY RZ
    omega = np.pi
    qp.RZ(omega, wires=0)

    # RETURN THE STATE
    return qp.state()
    
# ===== I.5.3 =====
dev = qp.device("default.qubit", wires=1)
@qp.qnode(dev)
def many_rotations():
    """Implement the circuit depicted above and return the quantum state.

    Returns:
        np.array[complex]: The state of the qubit after the operations.
    """
    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE CIRCUIT
    qp.Hadamard(wires=0)
    qp.S(wires=0)
    qp.adjoint(qp.T)(wires=0)
    qp.RZ(0.3, wires=0)
    qp.adjoint(qp.S)(wires=0)
    
    # RETURN THE STATE
    return qp.state()
