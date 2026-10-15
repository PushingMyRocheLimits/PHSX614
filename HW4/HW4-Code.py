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

print(apply_cnot(0))

#I.12.2 =====
dev = qp.device("default.qubit", wires=2)


@qp.qnode(dev)
def apply_h_cnot():
    ##################
    # YOUR CODE HERE #
    ##################

    qp.Hadamard(wires=0)
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

    qp.Hadamard(wires=0)

    qp.CRX(theta, wires=[0, 1])

    qp.CRY(phi, wires=[1, 2])

    qp.CRZ(omega, wires=[2, 0])

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

    qp.SWAP(wires=[0,1])

    return qp.state()


@qp.qnode(dev)
def apply_swap_with_cnots(phi, theta, omega):
    prepare_states(phi, theta, omega)

    ##################
    # YOUR CODE HERE #
    ##################

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

    qp.Hadamard(wires=0)
    qp.Hadamard(wires=1)
    qp.Hadamard(wires=2)

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

    qp.Toffoli(wires=[0, 1, 3])

    qp.Toffoli(wires=[2, 3, 4])

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

    qp.PauliX(wires=2)
    qp.Hadamard(wires=2)

    ##################
    # YOUR CODE HERE #
    ##################

    qp.ctrl(qp.PauliX, control=[0, 1], control_values=[0, 1])(wires=2)

    qp.ctrl(qp.PauliZ, control=[0, 1], control_values=[1, 0])(wires=2)

    qp.ctrl(qp.PauliY, control=[0, 1], control_values=[1, 1])(wires=2)

    return qp.state()


print(apply_control_sequence(state))

# A.1.1 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

@qp.qnode(dev)
def naive_circuit():
    """Create a uniform superposition and return the probabilities.

    Returns: 
        array[float]: Probabilities for observing different outcomes.
    """
    for wire in range(n_bits):

        ##################
        # YOUR CODE HERE #
        ##################
        qp.Hadamard(wires=wire)

    return qp.probs(wires=range(n_bits))

# A.2.1 ====

def oracle_matrix(combo):
    """Return the oracle matrix for a secret combination.
    
    Args:
        combo (list[int]): A list of bits representing a secret combination.
         
    Returns: 
        array[float]: The matrix representation of the oracle.
    """
    index = np.ravel_multi_index(combo, [2]*len(combo)) # Index of solution
    my_array = np.identity(2**len(combo)) # Create the identity matrix

    ##################
    # YOUR CODE HERE #
    ##################
    my_array[index, index] = -1.0

    return my_array

# A.2.2 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

@qp.qnode(dev)
def oracle_circuit(combo):
    """Create a uniform superposition, apply the oracle, and return probabilities.
    
    Args:
        combo (list[int]): A list of bits representing a secret combination.

    Returns:
        list[float]: The output probabilities.
    """

    ##################
    # YOUR CODE HERE #
    ##################
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))

    return qp.probs(wires=range(n_bits))

# A.3.1 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

@qp.qnode(dev)
def pair_circuit(x_tilde, combo):
    """Test a pair labelled by x_tilde for the presence of a solution.
    
    Args:
        x_tilde (list[int]): An (n_bits - 1)-string labelling the pair to test.
        combo (list[int]): A secret combination of n_bits 0s and 1s.
        
    Returns:
        array[float]: Probabilities on the last qubit.
    """
    for i in range(n_bits-1): # Initialize x_tilde part of state
        if x_tilde[i] == 1:
            qp.PauliX(wires=i)

    ##################
    # YOUR CODE HERE #
    ##################

    qp.Hadamard(wires=n_bits - 1)

    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))

    qp.Hadamard(wires=n_bits - 1)
    
    return qp.probs(wires=n_bits-1)

# A.3.2 ====

def pair_lock_picker(trials):
    """Create a combo, run pair_circuit until it succeeds, and tally success rate.
    
    Args:
        trials (int): Number of times to test the lock picker.

    Returns:
        float: The average number of times the lock picker uses pair_circuit.
    """
    x_tilde_strs = [np.binary_repr(n, n_bits-1) for n in range(2**(n_bits-1))]
    x_tildes = [[int(s) for s in x_tilde_str] for x_tilde_str in x_tilde_strs] 

    test_numbers = []

    for trial in range(trials):
        combo = secret_combo(n_bits) # Random list of bits
        counter = 0
        for x_tilde in x_tildes:
            counter += 1

            ##################
            # YOUR CODE HERE #
            ##################
            if pair_circuit(x_tilde, combo)[1] > 0.5:
                break
        
        test_numbers.append(counter)
    return sum(test_numbers)/trials

trials = 500
output = pair_lock_picker(trials)

print(f"For {n_bits} bits, it takes", output, "pair tests on average.")

# A.4.1 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

def multisol_oracle_matrix(combos):
    """Return the oracle matrix for a set of solutions.

    Args:
        combos (list[list[int]]): A list of secret bit strings.

    Returns:
        array[float]: The matrix representation of the oracle.
    """
    indices = [np.ravel_multi_index(combo, [2]*len(combo)) for combo in combos]
    ##################
    # YOUR CODE HERE #
    ##################
    my_array = np.identity(2 ** len(combos[0]))
    for index in indices:
        my_array[index, index] = -1.0

    return my_array

@qp.qnode(dev)
def multisol_pair_circuit(x_tilde, combos):
    """Implements the circuit for testing a pair of combinations labelled by x_tilde.
    
    Args:
        x_tilde (list[int]): An (n_bits - 1)-bit string labelling the pair to test.
        combos (list[list[int]]): A list of secret bit strings.

    Returns:
        array[float]: Probabilities on the last qubit.
    """
    for i in range(n_bits-1): # Initialize x_tilde part of state
        if x_tilde[i] == 1:
            qp.PauliX(wires=i)

    ##################
    # YOUR CODE HERE #
    ##################
    qp.Hadamard(wires=n_bits - 1)

    qp.QubitUnitary(multisol_oracle_matrix(combos), wires=range(n_bits))

    qp.Hadamard(wires=n_bits - 1)
    return qp.probs(wires=n_bits-1)

# A.4.2 ====

def parity_checker(combos):
    """Use multisol_pair_circuit to determine the parity of a solution set.

    Args:
        combos (list[list[int]]): A list of secret combinations.

    Returns: 
        int: The parity of the solution set.
    """
    parity = 0
    x_tilde_strs = [np.binary_repr(n, n_bits-1) for n in range(2**(n_bits-1))]
    x_tildes = [[int(s) for s in x_tilde_str] for x_tilde_str in x_tilde_strs]
    for x_tilde in x_tildes:

        ##################
        # YOUR CODE HERE #
        ##################

        # IMPLEMENT PARITY COUNTING ALGORITHM
        if multisol_pair_circuit(x_tilde, combos)[1] > 0.5:
            parity = (parity + 1) % 2

    return parity

# A.5.1 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

@qp.qnode(dev)
def hoh_circuit(combo):
    """A circuit which applies Hadamard-oracle-Hadamard and returns probabilities.
    
    Args:
        combo (list[int]): A list of bits representing a secret combination.

    Returns:
        list[float]: Measurement outcome probabilities.
    """

    ##################
    # YOUR CODE HERE #
    ##################
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    return qp.probs(wires=range(n_bits))

# A.6.1 ====

n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)

@qp.qnode(dev)
def multisol_hoh_circuit(combos):
    """A circuit which applies Hadamard, multi-solution oracle, then Hadamard.
    
    Args:
        combos (list[list[int]]): A list of secret bit strings.

    Returns: 
        array[float]: Probabilities for observing different outcomes.
    """

    ##################
    # YOUR CODE HERE #
    ##################
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    qp.QubitUnitary(multisol_oracle_matrix(combos), wires=range(n_bits))

    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    return qp.probs(wires=range(n_bits))

# A.6.2 ====

def deutsch_jozsa(promise_var):
    """Implement the Deutsch–Jozsa algorithm and guess the promise variable.
    
    Args:
        promise_var (int): Indicates whether the function is balanced (0) or constant (1).
        
    Returns: 
        int: A guess at the promise variable.
    """
    if promise_var == 0:
        how_many = 2**(n_bits - 1)
    else:
        how_many = np.random.choice([0, 2**n_bits]) # Choose all or nothing randomly
    combos = multisol_combo(n_bits, how_many) # Generate random combinations

    ##################
    # YOUR CODE HERE #
    ##################
    probs = multisol_hoh_circuit(combos)
    # If probability of measuring |00...0> is 1,  function is constant (1)
    # If probability of measuring |00...0> is 0,  function is balanced (0)
    if np.isclose(probs[0], 1.0):
        return 1
    else:
        return 0

