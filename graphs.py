import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import SparsePauliOp

def plot_vqe(energies, angle, title=""):
    #print("Entré a la función")
    fig, axs = plt.subplots(2,1)
    #iteration vs energy
    axs[0].plot(energies, marker = 'o')
    axs[0].set_title(f"{title} iteration vs energy")
    axs[0].set_xlabel('Iteration')
    axs[0].set_ylabel('Energy (MeV)')
    #axs[0].legend()
    axs[0].grid()
    #iteration vs angle
    axs[1].plot(angle, marker = 's')
    axs[1].set_title(f"{title} iteration vs angle")
    axs[1].set_xlabel('Iteration')
    axs[1].set_ylabel('Angle (radians)')
    #axs[1].legend()
    axs[1].grid()
    #plt.savefig('mi_grafica_prueba.png')
    plt.show()

def plot_energy(est, qca, H2):
    pauli_terms = [
    SparsePauliOp.from_list([("II", 1.0)]),
    SparsePauliOp.from_list([("IZ", 1.0)]),
    SparsePauliOp.from_list([("ZI", 1.0)]),
    SparsePauliOp.from_list([("XX", 1.0)]),
    SparsePauliOp.from_list([("YY", 1.0)])
    ]


    energies = []
    theta_groupe = np.linspace(-np.pi,np.pi, 50)
    pauli_expectations = { "IZ": [], "ZI": [], "XX": [], "YY": [] }

    # Energy vs angle
    for t in theta_groupe:
        par_total = (qca, H2, [t])
        res_total = est.run([par_total]).result()
        energies.append(float(res_total[0].data.evs))
        
        # Individuals terms
        for i, label in enumerate(["IZ", "ZI", "XX", "YY"]):
            par_term = (qca, pauli_terms[i+1], [t])
            res_term = est.run([par_term]).result()
            pauli_expectations[label].append(float(res_term[0].data.evs))


    fig, axs = plt.subplots(2,1)

    axs[0].plot(theta_groupe, energies)
    axs[0].set_title(" angle vs energy")
    axs[0].set_xlabel('Angle (radians)')
    axs[0].set_ylabel('Energy (MeV)')
    #axs[0].legend()
    axs[0].grid()

    labels =["IZ", "ZI", "XX", "YY"]
    for label in labels:
        axs[1].plot(theta_groupe,pauli_expectations[label], label = label, marker="o")

    axs[1].set_xlabel('Angle (radians)')
    axs[1].set_ylabel('Energy (MeV)')
    axs[1].legend()
    axs[1].grid()

    plt.show()


def plot_energy_n3(est, qcb, H3, eta_opt, theta_opt):
    pauli_ops = {
        "ZII": SparsePauliOp.from_list([("ZII", 1.0)]),
        "XXI": SparsePauliOp.from_list([("XXI", 1.0)]),
        "IZI": SparsePauliOp.from_list([("IZI", 1.0)]),
        "IIZ": SparsePauliOp.from_list([("IIZ", 1.0)])
    }

    angles_array = np.linspace(-np.pi, np.pi, 50)
    
    energies_theta = []
    paulis_theta = {label: [] for label in pauli_ops.keys()}
    
    energies_eta = []
    paulis_eta = {label: [] for label in pauli_ops.keys()}

    # THETA variable, ETA fixé
    for t in angles_array:
        par_total = (qcb, H3, [eta_opt, t])
        res = est.run([par_total]).result()
        energies_theta.append(float(res[0].data.evs))
        
        for label, op in pauli_ops.items():
            par_ind = (qcb, op, [eta_opt, t])
            res_term = est.run([par_ind]).result()
            paulis_theta[label].append(float(res_term[0].data.evs))

    # ETA variable, THETA fixé
    for e in angles_array:
        par_total = (qcb, H3, [e, theta_opt])
        res = est.run([par_total]).result()
        energies_eta.append(float(res[0].data.evs))
        
        for label, op in pauli_ops.items():
            par_ind = (qcb, op, [e, theta_opt])
            res_term = est.run([par_ind]).result()
            paulis_eta[label].append(float(res_term[0].data.evs))

    #graphs 
    fig, axs = plt.subplots(2, 2)

    #   THETA variable, ETA fixé
    axs[0, 0].plot(angles_array, energies_theta, color='black')
    axs[0, 0].set_title(f"Energy vs Theta (Eta fixé {eta_opt:.2f})")
    axs[0, 0].set_ylabel('Energy (MeV)')
    axs[0, 0].grid()

    for label in pauli_ops.keys():
        axs[1, 0].plot(angles_array, paulis_theta[label], label=label)
    axs[1, 0].set_xlabel('Theta (radians)')
    axs[1, 0].set_ylabel('Expectation Value')
    axs[1, 0].legend()
    axs[1, 0].grid()

    # ETA variable, THETA fixé
    axs[0, 1].plot(angles_array, energies_eta, color='black')
    axs[0, 1].set_title(f"Energy vs Eta (Theta fixé {theta_opt:.2f})")
    axs[0, 1].grid()

    for label in pauli_ops.keys():
        axs[1, 1].plot(angles_array, paulis_eta[label], label=label)
    axs[1, 1].set_xlabel('Eta (radians)')
    axs[1, 1].legend()
    axs[1, 1].grid()

    plt.tight_layout()
    plt.show()

def plot_n3_ZNE(r, energies_r):
    plt.figure()
    plt.plot(r, energies_r, marker='^')

    m, b = np.polyfit(r, energies_r, 1)
    
    energie_0 = b 
    
    x_line = np.linspace(0, max(r), 50)
    y_line = m * x_line + b
    plt.plot(x_line, y_line, color='orange', linestyle='dashed', label=f"Linear Adjustment")
    plt.plot(0, energie_0, marker='*', markersize=15, markeredgecolor='black', label=f"Found value(r=0): {energie_0:.4f} MeV")
    plt.title("Zero-Noise Extrapolation (ZNE) N=3")
    plt.xlabel(" Noise factor(r CNOTs)")
    plt.ylabel("Mesured energy  (MeV)")
    plt.legend()
    plt.xticks([0] + r)
    plt.xticks(r)
    plt.grid(True)
    plt.show()