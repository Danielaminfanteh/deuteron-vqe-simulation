from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
from hamiltonian import H2_function, H3_function
from ansatz import ansatz_n2_function, ansatz_n3_function, ansatz_bruit_n2, ansatz_bruit_n3
from graphs import plot_energy, plot_vqe, plot_energy_n3, plot_n3_ZNE
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_aer.primitives import Estimator as AerEstimator
#from qiskit.providers.fake_provider import FakeManilaV2
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit.providers.fake_provider import GenericBackendV2

def run_vqe_n2():
    H2 = H2_function()
    qca, parameters = ansatz_n2_function()
    est = StatevectorEstimator()

    angle =[]
    energies =[]

    def energy_f(theta):
        par = (qca, H2, theta)
        work = est.run([par])
        resultat = work.result() #me donne une list de resultats pour chauqe element 
        energy_v = float(resultat[0].data.evs)
        energies.append(energy_v)
        angle.append(float(theta[0]))
        return energy_v


    #Initiation theta
    theta_0 = [0.0]
    #VQE
    result_vqe = minimize(energy_f, theta_0, method='COBYLA')
    print("\n--- RESULTATS FINALS ---")
    print("Theta optimisé trouvé:", result_vqe.x)
    print("Energie minimum pour le Deuteron:", result_vqe.fun, "MeV")
    print("llegue a las graphs")
    plot_vqe(energies, angle, title="N=2")
    plot_energy(est, qca, H2)

    return result_vqe.x


def run_vqe_n3():
    H3 = H3_function()
    qcb, parameters = ansatz_n3_function()
    est = StatevectorEstimator()

    angle_t =[]
    angle_e = []
    energy =[]
    def energy_N3(angles):
        eta = float(angles[0])
        theta= float(angles[1])
        par = (qcb, H3, [eta, theta])
        work = est.run([par]) #On active le circuit 
        resultat = work.result() #me donne une list de resultats pour chauqe element, dans ce cas on l'a donné juste un devoir, du couo il y a juste un valeur attendu.
        energy_v = float(resultat[0].data.evs) #Ici on prend ce premier element comme un numéro.
        energy.append(energy_v)
        angle_t.append(float(theta))
        angle_e.append(float(eta))
        return energy_v

    #minimization
    #Initiation theta and eta
    initial_angles = [0.0, 0.0]

    #VQE
    result3_vqe = minimize(energy_N3, initial_angles, method='COBYLA')
    print("\n--- RESULTATS FINALS ---")
    print("Theta optimisé trouvé:", result3_vqe.x[1])
    print("Eta optimisé trouvé:  ", result3_vqe.x[0])
    print("Energie minimum pour le Deuteron:", result3_vqe.fun, "MeV")

    plot_vqe(energy, angle_e, title="N=3 (eta)")
    plot_vqe(energy, angle_t, title="N=3 (Theta)")
    plot_energy_n3(est, qcb, H3, result3_vqe.x[0], result3_vqe.x[1])

    return result3_vqe.x[0], result3_vqe.x[1]

#bruit: 1. Creer estimateur avec du bruit de 2% chaque fois que on applique un CNOT , apres changer l'estimateur dans la fonction d'avant. Très ideal. 

# def function_est_r():
#     model_r = NoiseModel()
#     error_cnot = depolarizing_error(0.02, 2) #Taux d'erreur. 2% est realiste pour les chips actuales. C'est appliqué a gates de 2 qubits.
#     model_r.add_all_qubit_quantum_error(error_cnot, ['cx'])
#     est_r = AerEstimator( backend_options={"noise_model": model_r},transpile_options={"optimization_level": 0}, approximation=True )
#     return est_r

def function_est_r():
    #chip_ibm = FakeManilaV2()
    chip_ibm = GenericBackendV2(num_qubits=5)
    model_r = NoiseModel.from_backend(chip_ibm)
    est_r = AerEstimator( backend_options={"noise_model": model_r}, transpile_options={"optimization_level": 0}, approximation=True)
    return est_r
def run_zne_n3(eta_opt, theta_opt):
    H3 = H3_function()
    est_r = function_est_r() 
    
    nivels_r = [1, 3, 5, 7]
    energies_r = []

    for r in nivels_r:
        qcb_r, params = ansatz_bruit_n3(r) 
        res = est_r.run(circuits=[qcb_r], observables=[H3], parameter_values=[[eta_opt, theta_opt]]).result()
        energy = float(res.values[0])
        energies_r.append(energy)
        print(f"Niveau r={r} ({r} CNOTs): Energie = {energy:.4f} MeV")
    plot_n3_ZNE(nivels_r, energies_r)
    


    

if __name__ == "__main__":
    run_vqe_n2()
    eta_final, theta_final = run_vqe_n3()
    run_zne_n3(eta_final, theta_final)

