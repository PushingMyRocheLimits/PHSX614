# ==== P.4.1 ====
dev = qp.device("default.qubit", wires=5)
estimation_wires = [0, 1, 2]
target_wires = [3]

def prepare_eigenvector_superposition(alpha, beta):
    # Normalize alpha and beta
    norm_squared = np.abs(alpha) ** 2 + np.abs(beta) ** 2
    norm = np.sqrt(norm_squared)
    state = np.array([alpha/norm, beta/norm])

    # Prepare the state
    qp.MottonenStatePreparation(state, wires=target_wires)


@qp.qnode(dev)
def qpe(unitary):
    """Estimate the phase for a given unitary.

    Args:
        unitary (array[complex]): A unitary matrix.

    Returns:
        array[float]: Probabilities on the estimation wires.
    """

    # MODIFY ALPHA, BETA TO PREPARE EIGENVECTOR
    prepare_eigenvector_superposition(0, 1)
    # prepare_eigenvector_superposition(1, 0)
    # prepare_eigenvector_superposition(1/np.sqrt(2), 1/np.sqrt(2))
    # OR UNCOMMENT LINES ABOVE TO PREPARE THE STATE OF YOUR CHOICE

    qp.QuantumPhaseEstimation(
        unitary,
        target_wires=target_wires,
        estimation_wires=estimation_wires,
    )
    return qp.probs(wires=estimation_wires)

U = qp.T.compute_matrix()

probs = qpe(U)

# Save the target phase index before execution
target_index = np.argmax(probs)

# Convert the highest probability binary string index into a phase angle estimate:
# phase = index / 2^(num_estimation_wires)
estimated_phase = target_index / (2 ** len(estimation_wires))

# Modify to True when you are done testing
done = True

# ==== p.4.2 ====
dev = qp.device("default.qubit", wires=5)
estimation_wires = [0, 1, 2]
target_wires = [3, 4]

def prepare_eigenvector_superposition(alpha, beta, gamma, delta):
    # Normalize alpha, beta, gamma, and delta
    norm_squared = np.abs(alpha) ** 2 + np.abs(beta) ** 2 + np.abs(gamma) ** 2 + np.abs(delta) ** 2
    norm = np.sqrt(norm_squared)
    state = np.array([alpha/norm, beta/norm, gamma/norm, delta/norm])

    #Prepare the state
    qp.MottonenStatePreparation(state, wires=target_wires)


@qp.qnode(dev)
def qpe(unitary):
    """Estimate the phase for a given unitary.

    Args:
        unitary (array[complex]): A unitary matrix.

    Returns:
        array[float]: Probabilities on the estimation wires.
    """

    # PREPARE EIGENVECTOR
    #prepare_eigenvector_superposition(0, 0, 0, 1)
    prepare_eigenvector_superposition(1, 1, 1, 1)
    # prepare_eigenvector_superposition(1, 0, 0, 0)


    qp.QuantumPhaseEstimation(
        unitary,
        target_wires=target_wires,
        estimation_wires=estimation_wires,
    )
    return qp.probs(wires=estimation_wires)


U = qp.CZ.compute_matrix()

probs = qpe(U)

# MODIFY TO PROBABILITY OF OBSERVING 100 WHEN ESTIMATION
# WIRES ARE IN EQUAL SUPERPOSITION
#probability_100 = 0.0
probability_100 = 0.25

# ==== P.4.3 ====
dev = qp.device("default.qubit", wires=6)
estimation_wires = [0, 1, 2, 3]
target_wires = [4, 5]

def prepare_eigenvector_superposition(alpha, beta, gamma, delta):
    # Normalize alpha, beta, gamma, and delta
    norm_squared = np.abs(alpha) ** 2 + np.abs(beta) ** 2 + np.abs(gamma) ** 2 + np.abs(delta) ** 2
    norm = np.sqrt(norm_squared)
    state = np.array([alpha/norm, beta/norm, gamma/norm, delta/norm])

    # Prepare the state
    qp.MottonenStatePreparation(state, wires=target_wires)


@qp.qnode(dev)
def qpe(unitary):
    """Estimate the phase for a given unitary.

    Args:
        unitary (array[complex]): A unitary matrix.

    Returns:
        probs (array[float]): Probabilities on the estimation wires.
    """

    # MODIFY ALPHA, BETA, GAMMA, DELTA TO PREPARE EIGENVECTOR
    #prepare_eigenvector_superposition(0, 0, 0, 1)
    # prepare_eigenvector_superposition(1, 0, 0, 0)
    # prepare_eigenvector_superposition(0, 1, 0, 0)
    prepare_eigenvector_superposition(1, 1, 1, 1)
    # OR UNCOMMENT LINES ABOVE TO PREPARE THE STATE OF YOUR CHOICE

    qp.QuantumPhaseEstimation(
        unitary,
        target_wires=target_wires,
        estimation_wires=estimation_wires,
    )
    return qp.probs(wires=estimation_wires)


# UNCOMMENT THE LINE CORRESPONDING TO THE MATRIX YOU'D LIKE
# TO ESTIMATE PHASES OF
#U = qp.CZ.compute_matrix()
U = qp.CRX.compute_matrix(1/3)
# U = qp.CRZ.compute_matrix(0.4)
# U = qp.CRX.compute_matrix(0.1)
# U = qp.CRot.compute_matrix(0.9, 0.7, 0.4)

probs = qpe(U)

#mystery_phase = 0.0 # MODIFY THIS
sorted_indices = np.argsort(probs)[::-1]
mystery_phase = sorted_indices[1] / 16

# ==== G.1.1 ====
n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)


def oracle_matrix(combo):
    """Return the oracle matrix for a secret combination.

    Args:
        combo (list[int]): A list of bits representing a secret combination.

    Returns:
        array[float]: The matrix representation of the oracle.
    """
    index = np.ravel_multi_index(combo, [2] * len(combo))  # Index of solution
    my_array = np.identity(2 ** len(combo))  # Create the identity matrix
    my_array[index, index] = -1
    return my_array


@qp.qnode(dev)
def oracle_amp(combo):
    """Prepare the uniform superposition and apply the oracle.

    Args:
        combo (list[int]): A list of bits representing the secret combination.

    Returns:
        array[complex]: The quantum state (amplitudes) after applying the oracle.
    """
    # 1. Apply Hadamard gates to all wires to create uniform superposition |+>^{\otimes n}
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    # 2. Apply the oracle matrix using QubitUnitary acting on all wires
    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))

    return qp.state()

# ==== G.1.2a ====
n_bits = 4
dev = qp.device("default.qubit", wires=n_bits)


def diffusion_matrix():
    """Return the diffusion matrix.

    Returns:
        array[float]: The matrix representation of the diffusion operator.
    """
    N = 2 ** n_bits
    # 2 * |s><s| where |s><s| is a matrix of all 1/N entries
    two_s_s_dag = (2 / N) * np.ones((N, N))

    # D = 2|s><s| - I
    D = two_s_s_dag - np.identity(N)
    return D


@qp.qnode(dev)
def difforacle_amp(combo):
    """Apply the oracle and diffusion matrix to the uniform superposition.

    Args:
        combo (list[int]): A list of bits representing the secret combination.

    Returns:
        array[complex]: The quantum state (amplitudes) after applying the oracle
        and diffusion.
    """
    # 1. Prepare uniform superposition |s> = |+>^{\otimes n}
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    # 2. Apply oracle operator U_w
    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))

    # 3. Apply Grover diffusion operator D
    qp.QubitUnitary(diffusion_matrix(), wires=range(n_bits))

    return qp.state()

# ==== G.1.2b ====
@qp.qnode(dev)
def two_difforacle_amp(combo):
    """Apply the Grover operator twice to the uniform superposition.

    Args:
        combo (list[int]): A list of bits representing the secret combination.

    Returns:
        array[complex]: The resulting quantum state.
    """
    # 1. Prepare uniform superposition |s> = |+>^{\otimes n}
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    # 2. First Grover Iteration (Oracle + Diffusion)
    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))
    qp.QubitUnitary(diffusion_matrix(), wires=range(n_bits))

    # 3. Second Grover Iteration (Oracle + Diffusion)
    qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))
    qp.QubitUnitary(diffusion_matrix(), wires=range(n_bits))

    return qp.state()

# ==== G.2.1 ====
n_bits = 5
dev = qp.device("default.qubit", wires=n_bits)


def oracle_matrix(combo):
    """Return the oracle matrix for a secret combination.

    Args:
        combo (list[int]): A list of bits representing a secret combination.

    Returns:
        array[float]: The matrix representation of the oracle.
    """
    index = np.ravel_multi_index(combo, [2] * len(combo))  # Index of solution
    my_array = np.identity(2 ** len(combo))  # Create the identity matrix
    my_array[index, index] = -1
    return my_array


def diffusion_matrix():
    """Return the diffusion matrix.

    Returns:
        array[float]: The matrix representation of the diffusion operator.
    """
    psi_piece = (1 / 2**n_bits) * np.ones((2**n_bits, 2**n_bits))
    ident_piece = np.eye(2**n_bits)
    return 2 * psi_piece - ident_piece


@qp.qnode(dev)
def grover_circuit(combo, num_steps):
    """Apply the Grover operator num_steps times to the uniform superposition
       and return the state.

    Args:
        combo (list[int]): A list of bits representing the secret combination.
        num_steps (int): The number of iterations of the Grover operator
            our circuit is to perform.

    Returns:
        array[complex]: The quantum state (amplitudes) after repeated Grover
        iterations.
    """
    # 1. Prepare uniform superposition |s> = |+>^{\otimes n}
    for wire in range(n_bits):
        qp.Hadamard(wires=wire)

    # 2. Repeat Grover iteration (Oracle + Diffusion) num_steps times
    for _ in range(num_steps):
        qp.QubitUnitary(oracle_matrix(combo), wires=range(n_bits))
        qp.QubitUnitary(diffusion_matrix(), wires=range(n_bits))

    return qp.state()


# Optimal number of Grover steps for 5 qubits is floor((pi/4) * sqrt(2^5)) = 4
my_steps = 4

# ==== G.3.1 ====
n_bits = 5
query_register = list(range(n_bits))
aux = [n_bits]
all_wires = query_register + aux
dev = qp.device("default.qubit", wires=all_wires)


def oracle(combo):
    """Implement an oracle using a multi-controlled X gate.

    Args:
        combo (list): A list of bits representing the secret combination.
    """
    combo_str = "".join(str(j) for j in combo)

    # 1. Flip qubits where the secret bit is '0' so all controls activate on '1'
    for i, bit in enumerate(combo_str):
        if bit == "0":
            qp.PauliX(wires=query_register[i])

    # 2. Apply MultiControlledX targeting the aux wire, controlled by query_register
    qp.MultiControlledX(wires=query_register + aux)

    # 3. Uncompute the PauliX gates to restore the query register
    for i, bit in enumerate(combo_str):
        if bit == "0":
            qp.PauliX(wires=query_register[i])

# ==== G.3.2 ====
def hadamard_transform(my_wires):
    """Apply the Hadamard transform on a given set of wires.

    Args:
        my_wires (list[int]): A list of wires on which the Hadamard transform will act.
    """
    for wire in my_wires:
        qp.Hadamard(wires=wire)


def diffusion():
    """Implement the diffusion operator using the Hadamard transform and
    multi-controlled X."""

    # 1. Apply Hadamard transform to the query register to move to computational basis
    hadamard_transform(query_register)

    # 2. Apply PauliX to all query wires so |00...0> becomes |11...1>
    for wire in query_register:
        qp.PauliX(wires=wire)

    # 3. Apply MultiControlledX targeting the aux wire (phase flip via aux state |->)
    qp.MultiControlledX(wires=query_register + aux)

    # 4. Uncompute PauliX gates on the query register
    for wire in query_register:
        qp.PauliX(wires=wire)

    # 5. Apply Hadamard transform back to the query register
    hadamard_transform(query_register)

# ==== G.3.3 ====
@qp.qnode(dev)
def grover_circuit(combo):
    """Apply the MultiControlledX Grover operator and return probabilities on
    query register.

    Args:
        combo (list[int]): A list of bits representing the secret combination.

    Returns:
        array[float]: Measurement outcome probabilities.
    """
    # 1. Prepare uniform superposition on query register
    hadamard_transform(query_register)

    # 2. Prepare auxiliary qubit in the |-> state: |0> --PauliX--> |1> --Hadamard--> |->
    qp.PauliX(wires=aux)
    hadamard_transform(aux)

    # 3. Single Grover Iteration: Oracle followed by Diffusion
    oracle(combo)
    diffusion()

    return qp.probs(wires=query_register)

# ==== G.4.1a ====
def grover_iter(combo, num_steps):
    """Run Grover search for a given secret combination and a number of iterations.

    Args:
        combo (list[int]): The secret combination, represented as a list of bits.
        num_steps (int): The number of Grover iterations to perform.

    Returns:
        array[float]: Probability for observing different outcomes.
    """
    n_bits = len(combo)
    query_register = list(range(n_bits))
    aux = [n_bits]
    all_wires = query_register + aux
    dev = qp.device("default.qubit", wires=all_wires)

    @qp.qnode(dev)
    def inner_circuit():
        # 1. Prepare uniform superposition on query register
        hadamard_transform(query_register)

        # 2. Prepare auxiliary qubit in the |-> state
        qp.PauliX(wires=aux)
        hadamard_transform(aux)

        # 3. Apply num_steps Grover iterations (Oracle + Diffusion)
        for _ in range(num_steps):
            oracle(combo)
            diffusion(n_bits)

        return qp.probs(wires=query_register)

    return inner_circuit()

# ==== G.4.1b ====
n_list = range(3, 7)
opt_steps = []

for n_bits in n_list:
    combo = [0] * n_bits  # A simple combination
    step_list = range(1, 10)  # Try out some large number of steps

    # Track target state [0...0] probability across step count
    target_probs = []
    for steps in step_list:
        probs = grover_iter(combo, steps)
        # Index 0 corresponds to computational basis state [0, 0, ..., 0]
        target_probs.append(probs[0])

    # Find position of the first local maximum (1-indexed)
    optimal_step = local_max_arg(target_probs)
    opt_steps.append(optimal_step)

print("The optimal number of Grover steps for qubits in", [3, 4, 5, 6], "is", opt_steps, ".")

# ==== G.4.2 ====
grad = 0.5
intercept = -0.47
# SUBMIT TO PLOT GRAPH

# ==== G.5.1 ====
n_bits = 5
query_register = list(range(n_bits))
aux = [n_bits]
all_wires = query_register + aux
dev = qp.device("default.qubit", wires=all_wires)


def oracle_multi(combos):
    """Implement multi-solution oracle using sequence of multi-controlled X gates.

    Args:
        combos (list[list[int]]): A list of solutions.
    """
    for combo in combos:

        ##################
        # YOUR CODE HERE #
        ##################
        qp.MultiControlledX(wires=all_wires, control_values=combo)

# ==== G.5.2a ====
n_bits = 5
query_register = list(range(n_bits))
aux = [n_bits]
all_wires = query_register + aux
dev = qp.device("default.qubit", wires=all_wires, shots=None)


def grover_iter_multi(combos, num_steps):
    """Run Grover search for multiple secret combinations and a number
    of Grover steps.

    Args:
        combos (list[list[int]]): The secret combination, represented as a list of bits.
        num_steps (int): The number of Grover iterations to perform.

    Returns:
        array[float]: Probability for observing different outcomes.
    """

    @qp.qnode(dev)
    def inner_circuit():
        qp.PauliX(wires=n_bits)
        qp.Hadamard(wires=n_bits)
        hadamard_transform(query_register)

        for _ in range(num_steps):
            ##################
            # YOUR CODE HERE #
            ##################
            oracle_multi(combos)
            diffusion(n_bits)
        return qp.probs(wires=query_register)

    return inner_circuit()

# ==== G.5.2b ====
m_list = range(3)
opt_steps = []

for m_bits in m_list:
    combos = [[int(s) for s in np.binary_repr(j, n_bits)] for j in range(2**m_bits)]
    step_list = range(1, 10)
    ##################
    # YOUR CODE HERE #
    ##################
    target_probs = []
    for steps in step_list:
        probs = grover_iter_multi(combos, steps)
        target_probs.append(probs[0])

    # Find the 1-indexed position of the first local maximum
    optimal_step = local_max_arg(target_probs)
    opt_steps.append(optimal_step)

print("The optimal number of Grover steps for the number of solutions in", [1, 2, 4], "is", opt_steps, ".")

# ==== G.5.3 ====
grad = -0.5
intercept = 2.03
# SUBMIT TO PLOT GRAPH
