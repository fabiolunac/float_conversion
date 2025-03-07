import struct
import math
import numpy as np

def generare_coeffs(nb_mant: int, nb_expo: int, print_coeffs: bool):
    n_bits = nb_mant + nb_expo + 1

    #-------------- Definição dos coeficientes --------------#

    # Numerador
    Znti = [4.294341492410895e-23,
                2.410259936829204e-09,
                    1.361884841455440e-08,
                        -4.120546556616038e-09,
                            -9.988893287934183e-09,
                                -1.906299572480522e-09,
                                    -1.381565400439083e-11,
                                        -2.560176577052387e-17,
                                                                0]

    # Denominador
    Zdti = [1.444400000000000e-08,
            -4.944897983017996e-09,
                -8.723804374709209e-09,
                    -5.868442605271617e-10,
                        -3.124085233920797e-10,
                            -6.992432687036571e-11,
                                2.478522822801157e-10,
                                        -2.439636477041001e-13,
                                            8.276140953857137e-26]

    #Normalização dos coeficientes
    b = np.zeros(len(Znti))
    a = np.zeros(len(Zdti))
    a_neg = np.zeros(len(Zdti))

    a0 = Zdti[0]
    Znti_norm = [i / a0 for i in Znti]
    Zdti_norm = [j / a0 for j in Zdti]

    #Conversão para float
    
    for i in range(len(Znti_norm)-1):
        b[i] = f2mf(Znti_norm[i], nb_mant, nb_expo)
        if print_coeffs == True:
            print(f" parameter [MAN+EXP:0] b{i} = {n_bits}'h{hex(int(b[i]))[2:]},")

    

    for i in range(1,len(Zdti_norm)):
        a[i] = f2mf(Zdti_norm[i], nb_mant, nb_expo)
        if print_coeffs == True:
            print(f" parameter [MAN+EXP:0] a{i} = {n_bits}'h{hex(int(a[i]))[2:]},")

    

    for i in range(1,len(a)):
        a_neg[i] = inverter_primeiro_bit(int(a[i]), n_bits)
        if print_coeffs == True:
            print(f" parameter [MAN+EXP:0] a{i}_neg = {n_bits}'h{hex(int(a_neg[i]))[2:]},")

    return Znti_norm, Zdti_norm




def inverter_primeiro_bit(num: int, num_bits: int) -> int:
    mask = 1 << (num_bits - 1)  # Cria uma máscara com o primeiro bit ligado
    return num ^ mask  # Inverte o primeiro bit com XOR



def f2mf(va: str, nbmant: int, nbexpo: int) -> int:
    f = float(va)
    
    if f == 0.0:
        return 1 << (nbmant + nbexpo - 1)
    
    # Converte float para representação IEEE 754 (bits)
    ifl = struct.unpack('!I', struct.pack('!f', f))[0]
    
    # Desempacotando IEEE 754
    s = (ifl >> 31) & 0x00000001
    e = ((ifl >> 23) & 0xFF) - 127 - 22
    m = ((ifl & 0x007FFFFF) + 0x00800000) >> 1
    
    # Sinal
    s = s << (nbmant + nbexpo)
    
    # Expoente
    e = e + (23 - nbmant)
    sh = 0
    
    while e < -math.pow(2, nbexpo - 1):
        e += 1
        sh += 1
    
    e = e & (int(math.pow(2, nbexpo)) - 1)
    e = e << nbmant
    
    # Mantissa
    if nbmant == 23:
        if ifl & 0x00000001:
            m += 1  # Arredonda
    else:
        sh = 23 - nbmant + sh
        carry = (m >> (sh - 1)) & 0x00000001
        m = m >> sh
        if carry:
            m += 1  # Arredonda
    
    return s + e + m



def mf2f(val: int , nbmant: int, nbexpo: int) -> float:
    """
    Função para converter o formato de ponto flutuante digital para float
    """
    
    s = (val >> (nbmant + nbexpo)) & 0x1
    e = (val >> nbmant) & ((1 << nbexpo) - 1)
    m = val & ((1 << nbmant) - 1)

    if e & (1 << nbexpo - 1):
        e_complemented = -((~e + 1) & (1 << nbexpo) - 1)
    else:
        e_complemented = e

    value = math.pow(-1, s) * m * math.pow(2, e_complemented)

    return value



def read_file(path:str):

    values_out = []

    with open(path, "r") as file:
        values_out = [int(linha.strip(),16) for linha in file]  # Remove espaços e quebras de linha

    return values_out