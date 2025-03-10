from funcoes import read_file, f2mf, mf2f, generare_coeffs
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pandas as pd

#-------------- Variáveis --------------#

nbmant = 23
nbexpo = 8
nbits = nbmant + nbexpo + 1

outlier_limit = 500

nbits_array = [12, 14, 16, 18, 20, 24, 28, 32]

print_coeffs = False
generate_graph = True

bit_config = {
#Bits :(Mantissa, Expoente)
    12: (7, 4),
    14: (7, 6),
    16: (9, 6),
    18: (10, 7),
    20: (11, 8),
    24: (15, 8),
    28: (19, 8),
    32: (23, 8)
}

def calculate_bits(nbits):
    return bit_config.get(nbits, (None, None))

#-------------- Coeficientes --------------#

Znti_norm, Zdti_norm = generare_coeffs(nbmant, nbexpo, print_coeffs)

#-------------- Definição do Impulso --------------#

N = 100
x = np.zeros(N)
x[0] = 1

y_ideal = signal.lfilter(Znti_norm, Zdti_norm, x)

energy_ideal = np.sum(y_ideal**2)

iir_file = np.zeros((len(nbits_array), N))  
iir_file_float = np.zeros((len(nbits_array), N))  
iir_filtered = np.zeros((len(nbits_array), N))  
error = np.zeros((len(nbits_array), N))  

error_energy = np.zeros(len(nbits_array))
error_factor = np.zeros(len(nbits_array))
error_mean = np.zeros(len(nbits_array))


#-------------- Leitura dos Dados Digitais --------------#

for i in range(len(nbits_array)):
    iir_path = f'files/filter_{nbits_array[i]}.txt'
    dados = read_file(iir_path)

    dados = dados[:N]

    iir_file[i,:] = dados


#-------------- Conversão para float --------------#
for i in range(len(nbits_array)):
    for j in range(N):
        iir_file_float[i,j] = mf2f(int(iir_file[i,j]), calculate_bits(nbits_array[i])[0], calculate_bits(nbits_array[i])[1])

#-------------- Removendo Outliers --------------#
iir_filtered = iir_file_float.copy()

for i in range(len(nbits_array)):
    #Removendo outliers
    iir_filtered[np.abs(iir_filtered) > outlier_limit] = 0

    #Calculando erro
    error[i] = y_ideal - iir_filtered[i]

    #Energia do erro
    error_energy[i] = np.sum(error[i]**2)
    error_factor[i] = error_energy[i]/energy_ideal

    error_mean[i] = np.mean(np.abs(error[i]))

if generate_graph == True:
    plt.figure()
    plt.plot(nbits_array,error_factor*100, marker = 'o')
    plt.xticks(nbits_array)
    plt.xlabel('Número de bits')
    plt.ylabel('Erro (%)')
    plt.title('Erro Final (%)')
    plt.grid()

    plt.axhline(y=1, color = 'r', label = 'Erro = 1%')
    for i in range(len(nbits_array)):
        plt.text(nbits_array[i], error_factor[i] * 100 + 0.2, f"{error_factor[i] * 100:.5f}%", 
                ha='center', fontsize=8)
    plt.legend()

    plt.show()