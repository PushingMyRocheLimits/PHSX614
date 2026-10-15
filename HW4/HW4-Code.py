#I.12.1
num_wires = 2
dev = qp.device("default.qubit", wires=num_wires)


@qp.qnode(dev)
def apply_cnot(basis_id):
    """Apply a CNOT to |basis_id>.

    Args:
        basis_id (int): An integer value identifying the basis state to construct.

    Returns:
        np.array[complex]: The resulting state after applying CNOT|basis_id>.
    """

    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=num_wires)]
    qp.BasisState(bits, wires=[0, 1])

    ##################
    # YOUR CODE HERE #
    ##################

    # APPLY THE CNOT
    qp.CNOT(wires=[0, 1])

    return qp.state()


##################
# YOUR CODE HERE #
##################

# REPLACE THE BIT STRINGS VALUES BELOW WITH THE CORRECT ONES
#cnot_truth_table = {"00": "00", "01": "00", "10": "00", "11": "00"}
cnot_truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}


# Run your QNode with various inputs to help fill in your truth table
print(apply_cnot(0))
#I.12.2 =====
dev = qp.device("default.qubit", wires=2)


@qp.qnode(dev)
def apply_h_cnot():
    ##################
    # YOUR CODE HERE #
    ##################

    # APPLY THE OPERATIONS IN THE CIRCUIT
    # Apply Hadamard on qubit 0
    qp.Hadamard(wires=0)

    # Apply CNOT with control qubit 0 and target qubit 1
    qp.CNOT(wires=[0, 1])

    return qp.state()


print(apply_h_cnot())

##################
# YOUR CODE HERE #
##################

# SET THIS AS 'separable' OR 'entangled' BASED ON YOUR OUTCOME
state_status = "entangled"

#I.12.3 ====
dev = qp.device("default.qubit", wires=3)

@qp.qnode(dev)
def controlled_rotations(theta, phi, omega):
    """Implement the circuit above and return measurement outcome probabilities.

    Args:
        theta (float): A rotation angle
        phi (float): A rotation angle
        omega (float): A rotation angle

    Returns:
        np.array[float]: Measurement outcome probabilities of the 3-qubit
        computational basis states.
    """

    ##################
    # YOUR CODE HERE #
    ##################

    # APPLY THE OPERATIONS IN THE CIRCUIT AND RETURN MEASUREMENT PROBABILITIES
    # 1. Hadamard on qubit 0
    qp.Hadamard(wires=0)

    # 2. Controlled-Rx with control=0, target=1
    qp.CRX(theta, wires=[0, 1])

    # 3. Controlled-Ry with control=1, target=2
    qp.CRY(phi, wires=[1, 2])

    # 4. Controlled-Rz with control=2, target=0
    qp.CRZ(omega, wires=[2, 0])

    # 5. Return measurement probabilities for the 3-qubit basis states
    return qp.probs(wires=[0, 1, 2])


theta, phi, omega = 0.1, 0.2, 0.3
print(controlled_rotations(theta, phi, omega))

# I.13.1 ====

dev = qp.device("default.qubit", wires=2)

# Prepare a two-qubit state; change up the angles if you like
phi, theta, omega = 1.2, 2.3, 3.4


@qp.qnode(device=dev)
def true_cz(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE REGULAR CZ GATE HERE
    qp.CZ(wires=[0, 1])

    return qp.state()


@qp.qnode(dev)
def imposter_cz(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT CZ USING ONLY H AND CNOT
    qp.Hadamard(wires=1)
    qp.CNOT(wires=[0, 1])
    qp.Hadamard(wires=1)

    return qp.state()


print(f"True CZ output state {true_cz(phi, theta, omega)}")
print(f"Imposter CZ output state {imposter_cz(phi, theta, omega)}")

# I.13.2 ====

dev = qp.device("default.qubit", wires=2)

# Prepare a two-qubit state; change up the angles if you like
phi, theta, omega = 1.2, 2.3, 3.4


@qp.qnode(dev)
def apply_swap(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE REGULAR SWAP GATE HERE
    qp.SWAP(wires=[0,1])

    return qp.state()


@qp.qnode(dev)
def apply_swap_with_cnots(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE SWAP GATE USING A SEQUENCE OF CNOTS
    qp.CNOT(wires=[0, 1])
    qp.CNOT(wires=[1, 0])
    qp.CNOT(wires=[0, 1])
    

    return qp.state()


print(f"Regular SWAP state = {apply_swap(phi, theta, omega)}")
print(f"CNOT SWAP state = {apply_swap_with_cnots(phi, theta, omega)}")


# I.13.3 ====

dev = qp.device("default.qubit", wires=3)

# Prepare first qubit in |1>, and arbitrary states on the second two qubits
phi, theta, omega = 1.2, 2.3, 3.4


# A helper function just so you can visualize the initial state
# before the controlled SWAP occurs.
@qp.qnode(dev)
def no_swap(phi, theta, omega):
    prepare_states(phi, theta, omega)
    return qp.state()


@qp.qnode(dev)
def controlled_swap(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

    # PERFORM A CONTROLLED SWAP USING A SEQUENCE OF TOFFOLIS
    qp.Toffoli(wires=[0, 1, 2])
    qp.Toffoli(wires=[0, 2, 1])
    qp.Toffoli(wires=[0, 1, 2])

    return qp.state()


print(no_swap(phi, theta, omega))
print(controlled_swap(phi, theta, omega))

# I.13.4 ====

dev = qp.device("default.qubit", wires=4)


@qp.qnode(dev)
def four_qubit_mcx():
    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE CIRCUIT ABOVE USING A 4-QUBIT MULTI-CONTROLLED X
    qp.Hadamard(wires=0)
    qp.Hadamard(wires=1)
    qp.Hadamard(wires=2)

    # 2. Apply multi-controlled X gate with control values |001>
    qp.MultiControlledX(wires=[0, 1, 2, 3], control_values=[0, 0, 1])

    return qp.state()


print(four_qubit_mcx())


# I.13.5 ====

# Wires 0, 1, 2 are the control qubits
# Wire 3 is the auxiliary qubit
# Wire 4 is the target
dev = qp.device("default.qubit", wires=5)


@qp.qnode(dev)
def four_qubit_mcx_only_tofs():
    # We will initialize the control qubits in state |1> so you can see
    # how the output state gets changed.
    qp.PauliX(wires=0)
    qp.PauliX(wires=1)
    qp.PauliX(wires=2)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT A 3-CONTROLLED NOT WITH TOFFOLIS
    # 1. Compute AND of controls 0 and 1 into auxiliary wire 3
    qp.Toffoli(wires=[0, 1, 3])

    # 2. Compute AND of auxiliary wire 3 and control 2 into target wire 4
    qp.Toffoli(wires=[2, 3, 4])

    # 3. Uncompute auxiliary wire 3 back to |0>
    qp.Toffoli(wires=[0, 1, 3])

    return qp.state()


print(four_qubit_mcx_only_tofs())

# I.14.1 ====

dev = qp.device("default.qubit", wires=2)

# Starting from the state |00>, implement a PennyLane circuit
# to construct each of the Bell basis states.


@qp.qnode(dev)
def prepare_psi_plus():
    # PREPARE (1/sqrt(2)) (|00> + |11>)
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[0, 1])

    return qp.state()


@qp.qnode(dev)
def prepare_psi_minus():
    # PREPARE (1/sqrt(2)) (|00> - |11>)
    qp.PauliX(wires=0)
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[0, 1])

    return qp.state()


@qp.qnode(dev)
def prepare_phi_plus():
    # PREPARE (1/sqrt(2)) (|01> + |10>)
    qp.PauliX(wires=1)
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[0, 1])

    return qp.state()


@qp.qnode(dev)
def prepare_phi_minus():
    # PREPARE (1/sqrt(2)) (|01> - |10>)
    qp.PauliX(wires=0)
    qp.PauliX(wires=1)
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[0, 1])

    return qp.state()


psi_plus = prepare_psi_plus()
psi_minus = prepare_psi_minus()
phi_plus = prepare_phi_plus()
phi_minus = prepare_phi_minus()

# Uncomment to print results
# print(f"|ψ_+> = {psi_plus}")
# print(f"|ψ_-> = {psi_minus}")
# print(f"|ϕ_+> = {phi_plus}")
# print(f"|ϕ_-> = {phi_minus}")

# I.14.2 ====

dev = qp.device("default.qubit", wires=3)

# State of first 2 qubits
state = [0, 1]


@qp.qnode(device=dev)
def apply_control_sequence(state):
    # Set up initial state of the first two qubits
    if state[0] == 1:
        qp.PauliX(wires=0)
    if state[1] == 1:
        qp.PauliX(wires=1)

    # Set up initial state of the third qubit - use |->
    # so we can see the effect on the output
    qp.PauliX(wires=2)
    qp.Hadamard(wires=2)

    ##################
    # YOUR CODE HERE #
    ##################

    # IMPLEMENT THE MULTIPLEXER
    # IF STATE OF FIRST TWO QUBITS IS 01, APPLY X TO THIRD QUBIT
    qp.ctrl(qp.PauliX, control=[0, 1], control_values=[0, 1])(wires=2)

    # IF STATE OF FIRST TWO QUBITS IS 10, APPLY Z TO THIRD QUBIT
    qp.ctrl(qp.PauliZ, control=[0, 1], control_values=[1, 0])(wires=2)

    # IF STATE OF FIRST TWO QUBITS IS 11, APPLY Y TO THIRD QUBIT
    qp.ctrl(qp.PauliY, control=[0, 1], control_values=[1, 1])(wires=2)

    return qp.state()


print(apply_control_sequence(state))

# I.15.1 ====



# I.15.2 ====


