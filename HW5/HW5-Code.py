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


