from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def ansatz_n2_function():
    qca = QuantumCircuit(2)

    #Ansatz
    #X(0)
    qca.x(0)
    #Y(theta)
    theta = Parameter('θ')
    qca.ry(theta , 1)
    #CNOT(1,0)
    qca.cx(1,0)
    #print
    print("Circuit Ansatz a):")
    print(qca.draw())
    return qca, [theta]

def ansatz_n3_function():
    qcb = QuantumCircuit(3)
    #Ansatz 
    #X0
    qcb.x(0)
    #Y(eta)
    eta = Parameter('η')
    qcb.ry(eta , 1)
    #y(theta)
    theta = Parameter('θ')
    qcb.ry(theta, 2)
    #CNOT (2,0)
    qcb.cx(2,0)
    #CNOT (0,1)
    qcb.cx(0,1)
    #Y(-eta)
    qcb.ry(- eta, 1)
    #CNOT (0,1)
    qcb.cx(0,1)
    #CNOT (1,0)
    qcb.cx(1,0)

    #print
    print("Circuit Ansatz B):")
    print(qcb.draw())
    return qcb, [eta, theta]


#Ansatz avec bruit 
#####

def ansatz_bruit_n2(r):
    qca = QuantumCircuit(2)
    theta = Parameter('θ')
    
    qca.x(0)
    qca.ry(theta , 1)
    for _ in range(r):
        qca.cx(1,0)
    print(f"Circuit Ansatz N=2 avec niveau de bruit {r}:")
    print(qca.draw())
    return qca, [theta]



def ansatz_bruit_n3(r):
    qcb = QuantumCircuit(3)
    eta = Parameter('η')
    theta = Parameter('θ')


    qcb.x(0)
    qcb.ry(eta , 1)
    qcb.ry(theta, 2)

    for _ in range(r):
        qcb.cx(2,0)

    for _ in range(r):
        qcb.cx(0,1)

    qcb.ry(- eta, 1)
    for _ in range(r):
        qcb.cx(0,1)
    for _ in range(r):
        qcb.cx(1,0)

    print(f"Circuit Ansatz N=3 avec niveau de bruit {r}:")
    print(qcb.draw())
    return qcb, [eta, theta]


    