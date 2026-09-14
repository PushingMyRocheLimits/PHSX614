===== I.2.1 =====
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

===== I.2.2 ======
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

===== I.2.3 ======
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

===== I.2.4 ======
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
