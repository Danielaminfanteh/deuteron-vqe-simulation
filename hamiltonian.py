from qiskit.quantum_info import SparsePauliOp

def H2_function():
    H2 = SparsePauliOp.from_list([
    ("II", 5.906709),     #MeV
    ("IZ", 0.218291),     #MeV
    ("ZI", -6.125),       #MeV
    ("XX", -2.143304),    #MeV
    ("YY", -2.143304)     #MeV
])

    print(" H2 defini:", H2, "MeV")
    return H2
def H3_function():
    H3 =  SparsePauliOp.from_list([
        ("III", 9.625+5.906709),     #MeV
        ("ZII", -9.625),       #MeV
        ("XXI", -3.913119),    #MeV
        ("YYI", -3.913119),    #MeV
        ("IIZ", 0.218291),     #MeV
        ("IZI", -6.125),       #MeV
        ("IXX", -2.143304),    #MeV
        ("IYY", -2.143304)     #MeV
    ])
    return H3