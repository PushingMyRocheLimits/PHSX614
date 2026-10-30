# ==== F.1.1 ====
def coefficients_to_values(coefficients):
    """Returns the value representation of a polynomial
    
    Args:
        coefficients (array[complex]): a 1-D array of complex 
            coefficients of a polynomial with 
            index i representing the i-th degree coefficient

    Returns: 
        array[complex]: the value representation of the 
            polynomial 
    """
    ##################
    # YOUR CODE HERE #
    ################## 
    return np.fft.fft(coefficients)

A = [4, 3, 2, 1]
print(coefficients_to_values(A))

# ==== F.1.2 ====
def values_to_coefficients(values):
    """Returns the coefficient representation of a polynomial
    
    Args:
        values (array[complex]): a 1-D complex array with 
            the value representation of a polynomial 

    Returns: 
        array[complex]: a 1-D complex array of coefficients
    """
    
    ##################
    # YOUR CODE HERE #
    ################## 
    return np.fft.ifft(values)


A = [10.+0.j,  2.-2.j,  2.+0.j,  2.+2.j]
print(values_to_coefficients(A))
# ==== F.1.3 ====
def nearest_power_of_2(x):
    """Given an integer, return the nearest power of 2. 
    
    Args:
        x (int): a positive integer

    Returns: 
        int: the nearest power of 2 of x
    """
    ##################
    # YOUR CODE HERE #
    ################## 
    if x <= 1:
        return 1
    return 1 << (x - 1).bit_length()
# ==== F.1.4 ====
def fft_multiplication(poly_a, poly_b):
    """Returns the result of multiplying two polynomials
    
    Args:
        poly_a (array[complex]): 1-D array of coefficients 
        poly_b (array[complex]): 1-D array of coefficients 

    Returns: 
        array[complex]: complex coefficients of the product
            of the polynomials, with length equal to the
            nearest power of 2 (as returned by
            values_to_coefficients, including trailing zeros)
    """
    ##################
    # YOUR CODE HERE #
    ################## 

    # Calculate the number of values required
    required_length = len(poly_a) + len(poly_b) - 1

    # Figure out the nearest power of 2
    n = nearest_power_of_2(required_length)

    # Pad zeros to the polynomial
    poly_a_padded = np.pad(poly_a, (0, n - len(poly_a)))
    poly_b_padded = np.pad(poly_b, (0, n - len(poly_b)))

    # Convert the polynomials to value representation 
    values_a = coefficients_to_values(poly_a_padded)
    values_b = coefficients_to_values(poly_b_padded)

    # Multiply
    values_product = values_a * values_b

    # Convert back to coefficient representation
    return values_to_coefficients(values_product)
  
# ==== F.2.1 ====
num_wires = 1
dev = qp.device("default.qubit", wires=num_wires)

@qp.qnode(dev)
def one_qubit_QFT(basis_id):
    """A circuit that computes the QFT on a single qubit. 
    
    Args:
        basis_id (int): An integer value identifying 
            the basis state to construct.
    
    Returns:
        array[complex]: The state of the qubit after applying QFT.
    """
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=num_wires)]
    qp.BasisState(bits, wires=[0])

    ##################
    # YOUR CODE HERE #
    ##################
    qp.Hadamard(wires=0)
    return qp.state()


# ==== F.2.2 ====
num_wires = 2
dev = qp.device("default.qubit", wires=num_wires)

# Derive the 4x4 QFT matrix 
omega = np.exp(2j * np.pi / 4)  # e^(2πi/4) = i
qft_matrix = 0.5 * np.array([[omega**(j * k) for k in range(4)] for j in range(4)])

@qp.qnode(dev)
def two_qubit_QFT(basis_id):
    """A circuit that computes the QFT on two qubits using qp.QubitUnitary. 
    
    Args:
        basis_id (int): An integer value identifying the basis state to construct.
    
    Returns:
        array[complex]: The state of the qubits after the QFT operation.
    """
    
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=num_wires)]
    qp.BasisState(bits, wires=[0, 1])
    
    ##################
    # YOUR CODE HERE #
    ##################
    
    qp.QubitUnitary(qft_matrix, wires=[0, 1])
    return qp.state()
# ==== F.2.3 ====
num_wires = 2
dev = qp.device("default.qubit", wires=num_wires)

@qp.qnode(dev)
def decompose_two_qubit_QFT(basis_id):
    """A circuit that computes the QFT on two qubits using elementary gates.
    
    Args:
        basis_id (int): An integer value identifying the basis state to construct.
    
    Returns:
        array[complex]: The state of the qubits after the QFT operation.
    """
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=num_wires)]
    qp.BasisState(bits, wires=[0, 1])
    
    ##################
    # YOUR CODE HERE #
    ##################

    qp.Hadamard(wires=0)    
    qp.ControlledPhaseShift(np.pi / 2, wires=[1, 0])    
    qp.Hadamard(wires=1)
    qp.SWAP(wires=[0, 1])
    
    return qp.state()
# ==== F.3.1 ====
num_wires = 3
dev = qp.device("default.qubit", wires=num_wires)

@qp.qnode(dev)
def three_qubit_QFT(basis_id):
    """A circuit that computes the QFT on three qubits.
    
    Args:
        basis_id (int): An integer value identifying the basis state to construct.
        
    Returns:
        array[complex]: The state of the qubits after the QFT operation.
    """
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=num_wires)]
    qp.BasisState(bits, wires=[0, 1, 2])
    
    ##################
    # YOUR CODE HERE #
    ################## 
    qp.Hadamard(wires=0)
    qp.ControlledPhaseShift(np.pi / 2, wires=[1, 0])
    qp.ControlledPhaseShift(np.pi / 4, wires=[2, 0])
    qp.Hadamard(wires=1)
    qp.ControlledPhaseShift(np.pi / 2, wires=[2, 1])
    qp.Hadamard(wires=2)
    qp.SWAP(wires=[0, 2])

    return qp.state()
# ==== F.3.2 ====
dev = qp.device('default.qubit', wires=4)

            
def swap_bits(n_qubits):
    """A circuit that reverses the order of qubits, i.e.,
    performs a SWAP such that [q1, q2, ..., qn] -> [qn, ... q2, q1].
    
    Args:
        n_qubits (int): An integer value identifying the number of qubits.
    """
    ##################
    # YOUR CODE HERE #
    ##################
    for i in range(n_qubits // 2):
        qp.SWAP(wires=[i, n_qubits - 1 - i])

@qp.qnode(dev) 
def qft_node(basis_id, n_qubits):
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=n_qubits)]
    qp.BasisState(bits, wires=range(n_qubits))
    # qft_rotations(n_qubits)
    swap_bits(n_qubits)
    return qp.state()
# ==== F.3.3 ====
dev = qp.device('default.qubit', wires=4)

def qft_rotations(n_qubits):
    """A circuit performs the QFT rotations on the specified qubits.
    
    Args:
        n_qubits (int): An integer value identifying the number of qubits.
    """

    ##################
    # YOUR CODE HERE #
    ################## 
    for target in range(n_qubits):
        qp.Hadamard(wires=target)
        for control in range(target + 1, n_qubits):
            angle = np.pi / (2 ** (control - target))
            qp.ControlledPhaseShift(angle, wires=[control, target])

@qp.qnode(dev) 
def qft_node(basis_id, n_qubits):
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=n_qubits)]
    qp.BasisState(bits, wires=range(n_qubits))
    qft_rotations(n_qubits)
    swap_bits(n_qubits)
    return qp.state()

# ==== F.3.4 ====
dev = qp.device('default.qubit', wires=4)

def qft_recursive_rotations(n_qubits, wire=0):
    """A circuit that performs the QFT rotations on the specified qubits
        recursively.
        
    Args:
        n_qubits (int): An integer value identifying the number of qubits.
        wire (int): An integer identifying the wire 
                    (or the qubit) to apply rotations on.
    """

    ##################
    # YOUR CODE HERE #
    ################## 
    if wire >= n_qubits:
        return
    qp.Hadamard(wires=wire)
    for control in range(wire + 1, n_qubits):
        angle = np.pi / (2 ** (control - wire))
        qp.ControlledPhaseShift(angle, wires=[control, wire])
    qft_recursive_rotations(n_qubits, wire=wire + 1)

@qp.qnode(dev) 
def qft_node(basis_id, n_qubits):
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=n_qubits)]
    qp.BasisState(bits, wires=range(n_qubits))
    qft_recursive_rotations(n_qubits)
    swap_bits(n_qubits)
    return qp.state()
# ==== F.3.5 ====
dev = qp.device('default.qubit', wires=4)

@qp.qnode(dev)
def pennylane_qft(basis_id, n_qubits):
    """A that circuit performs the QFT using PennyLane's QFT template.
    
    Args:
        basis_id (int): An integer value identifying 
            the basis state to construct.
        n_qubits (int): An integer identifying the 
            number of qubits.
            
    Returns:
        array[complex]: The state after applying the QFT to the qubits.
    """
    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=n_qubits)]
    qp.BasisState(bits, wires=range(n_qubits))

    ##################
    # YOUR CODE HERE #
    ################## 
    qp.QFT(wires=range(n_qubits))

    return qp.state()
# ==== P.1.1 ====
dev = qp.device("default.qubit", wires=2)

@qp.qnode(dev)
def guess_the_unitary(unitary):
    """Given a unitary that performs a Z or a -Z operation
    on a qubit, guess which one it is.
    
    Args: 
        U (array[complex]): A unitary matrix, guaranteed to be either Z or -Z.
    
    Returns:
        array [int]:  Probabilities on  on the first qubit
        using qp.probs()
    """
    ##################
    # YOUR CODE HERE #
    ##################  
    qp.Hadamard(wires=0)
    qp.ControlledQubitUnitary(unitary, wires=[0, 1])
    qp.Hadamard(wires=0)

    return qp.probs(wires=0)
    

# Z gate 
U = qp.PauliZ.compute_matrix() 

# -Z gate
# U = (-1)*qp.PauliZ.compute_matrix()

print(guess_the_unitary(U))
# ==== P.1.2 ====
dev = qp.device("default.qubit", wires=2)
        
@qp.qnode(dev)
def phase_kickback_X(eigenvector):
    """ Given an eigenvector of X, 
    apply the phase kickback circuit to observe 
    the probabilities on the control wire
    
    Args: 
        eigenvector(String): A string "plus" or "minus" depicting 
        the eigenvector of X
    
    Returns:
        array[int]: Measurement outcome on the first qubit using qp.probs()
    """
    # Prepare |ψ>
    ##################
    # YOUR CODE HERE #
    ##################  
    
    if eigenvector == "plus":
        qp.Hadamard(wires=1)
    elif eigenvector == "minus":
        qp.PauliX(wires=1)
        qp.Hadamard(wires=1)

        # Phase kickback
    ##################
    # YOUR CODE HERE #
    ################## 
    qp.Hadamard(wires=0)
    qp.CNOT(wires=[0, 1])  
    qp.Hadamard(wires=0)
 
    return qp.probs(wires=[0])   

print(phase_kickback_X("plus"))
print(phase_kickback_X("minus"))

# MODIFY EIGENVALUES BELOW 
eigenvalue_of_X_plus = 1
eigenvalue_of_X_minus = -1
# ==== P.2.1 ====
def U_power_2k(unitary, k):
    """ Computes U at a power of 2k (U^2^k)
    
    Args: 
        unitary (array[complex]): A unitary matrix
    
    Returns: 
        array[complex]: the unitary raised to the power of 2^k
    """
    ##################
    # YOUR CODE HERE #
    ##################  
    for _ in range(k):
        unitary = np.matmul(unitary, unitary)
    return unitary
            

# Try out a higher power of U
U = qp.T.compute_matrix()
print(U)

U_power_2k(U, 2)

# ==== P.2.2 ====
estimation_wires = [0, 1, 2]
target_wires = [3]

def apply_controlled_powers_of_U(unitary):
    """A quantum function that applies the sequence of powers of U^2^k to
    the estimation wires.
    
    Args: 
        unitary (array [complex]): A unitary matrix
    """

    ##################
    # YOUR CODE HERE #
    ##################  
    for i, wire in enumerate(estimation_wires):
        power = len(estimation_wires) - 1 - i
        u_pow = U_power_2k(unitary, power)
        qp.ctrl(qp.QubitUnitary(u_pow, wires=target_wires), control=wire)

# ==== P.2.3 ====
dev = qp.device("default.qubit", wires=4)

estimation_wires = [0, 1, 2]
target_wires = [3]

def prepare_eigenvector():
    qp.PauliX(wires=target_wires)

@qp.qnode(dev)
def qpe(unitary):
    """ Estimate the phase for a given unitary.
    
    Args:
        unitary (array[complex]): A unitary matrix.
        
    Returns:
        array[float]: Measurement outcome probabilities on the estimation wires.
    """
    ##################
    # YOUR CODE HERE #
    ################## 
    prepare_eigenvector()
    for wire in estimation_wires:
        qp.Hadamard(wires=wire)
    apply_controlled_powers_of_U(unitary)
    qp.adjoint(qp.QFT)(wires=estimation_wires)
    return qp.probs(wires=estimation_wires)
    

U = qp.T.compute_matrix()
print(qpe(U))

# ==== P.2.4 ====
estimation_wires = [0, 1, 2]
target_wires = [3]

def estimate_phase(probs):
    """Estimate the value of a phase given measurement outcome probabilities
    of the QPE routine.
    
    Args: 
        probs (array[float]): Probabilities on the estimation wires.
    
    Returns:
        float: the estimated phase   
    """
    ##################
    # YOUR CODE HERE #
    ################## 
    most_likely_outcome = np.argmax(probs)
    return most_likely_outcome / len(probs)

U = qp.T.compute_matrix()

probs = qpe(U)


estimated_phase = estimate_phase(probs)
print(estimated_phase)

# ==== P.2.5 ====
dev = qp.device("default.qubit", wires=4)

estimation_wires = [0, 1, 2]
target_wires = [3]

def prepare_eigenvector():
    qp.PauliX(wires=target_wires)

@qp.qnode(dev)
def qpe(unitary):
    """Estimate the phase for a given unitary.
    
    Args:
        unitary (array[complex]): A unitary matrix.
        
    Returns:
        array[float]: Probabilities on the estimation wires.
    """
    
    prepare_eigenvector()
    
    ##################
    # YOUR CODE HERE #
    ################## 
    qp.QuantumPhaseEstimation(
        unitary,
        target_wires=target_wires,
        estimation_wires=estimation_wires
    )
    
    return qp.probs(wires=estimation_wires)


U = qp.T.compute_matrix()
probs = qpe(U)
print(estimate_phase(probs))

# ==== P.3.1 ====
dev = qp.device("default.qubit", wires=10)

def fractional_binary_to_decimal(binary_fraction, wires):
    return float(binary_fraction/ 2 ** len(wires))

def phase_window(probs, estimation_wires):
    """ Given an array of probabilities, return the phase window of the 
    unitary's eigenvalue
    
    Args: 
        probs (array[float]): Probabilities on the estimation wires.
        estimation_wires (list[int]): List of estimation wires
    
    Returns:
        (float, float): the lower and upper bound of the phase
    """

    ##################
    # YOUR CODE HERE #
    ################## 
    most_likely = np.argmax(probs)
    
    probs_copy = np.copy(probs)
    probs_copy[most_likely] = -1.0
    second_most_likely = np.argmax(probs_copy)
    
    bound_1 = fractional_binary_to_decimal(most_likely, estimation_wires)
    bound_2 = fractional_binary_to_decimal(second_most_likely, estimation_wires)
    
    return (bound_1, bound_2)


# Test your solution

# You can increase the number of estimation wires to a maximum of range(0, 9)
estimation_wires = range(0, 3)

# The target is set to the last qubit
target_wires = [9]

# Define the unitary
U = np.array([[1, 0], [0, np.exp((2*np.pi*1j/7))]])

probs = qpe(U, estimation_wires, target_wires)

print(phase_window(probs, estimation_wires))

# MODIFY TO TRUE AFTER TESTING YOUR SOLUTION
done = True

# ==== P.3.2 ====
dev = qp.device("default.qubit", wires=10)

def estimates_array(unitary):
    """ Given a unitary, return a list of its phase windows
    
    Args: 
        unitary (array[complex]): A unitary matrix.
    
    Returns:
        [(float, float)]: a list of phase windows for 2 to 9 
        estimation wires
    """

    estimates = []
    target_wires = [9]

    ##################
    # YOUR CODE HERE #
    ################## 
    for num_est in range(2, 10):
        estimation_wires = range(num_est)
        probs = qpe(unitary, estimation_wires, target_wires)
        estimates.append(phase_window(probs, estimation_wires))

    return estimates


# Define the unitary
U = np.array([[1, 0], [0, np.exp((2*np.pi*1j/7))]])

estimates_array(U)

###################
# SUBMIT FOR PLOT #
###################
