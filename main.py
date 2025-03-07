from funcoes import mf2f, read_file
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

nb_mantissa = 23
nb_expo = 8

# -------------- Coeficientes -------------- #
Zn1 = [-0.0030]
Zd1 = [1.0000, -0.9978]


# -------------- Definição do Sinal -------------- #
N = 100
x = np.zeros(N)
x[0] = 1

# -------------- Resposta ao Impulso Ideal -------------- #
y1_ideal = signal.lfilter(Zn1, Zd1, x)


# -------------- Leitura dos Sinais -------------- #
# IIR1
iir1_path = "iir1_out.txt"
iir1_out = read_file(iir1_path, nb_mantissa, nb_expo)

erro1 = y1_ideal - iir1_out[0:N]

plt.figure()
plt.subplot(211)
plt.stem(y1_ideal)
plt.title('Resposta ao Impulso Ideal')

plt.subplot(212)
plt.stem(iir1_out[0:N])
plt.title('Resposta ao Impulso Simulada')


