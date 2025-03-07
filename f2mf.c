// converte um numero float (escrito em uma string) em meu float
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int f2mf(char *va, int nbmant, int nbexpo)
{
    float f = atof(va);

    int nbits = nbmant + nbexpo + 1;

    if (f == 0.0) return 1 << (nbmant + nbexpo -1);
    
    // int ifl = (int)&f; // isso aqui ta perigoso
    int ifl;
    memcpy(&ifl, &f, nbits);

    // desempacota padrao IEEE ------------------------------------------------

    int s =  (ifl >> 31) & 0x00000001;
    int e = ((ifl >> 23) & 0xFF) - 127 - 22;
    int m = ((ifl & 0x007FFFFF) + 0x00800000) >> 1;


    // sinal ------------------------------------------------------------------

    s = s << (nbmant + nbexpo);

    // expoente ---------------------------------------------------------------

    e = e + (23-nbmant);

    int sh = 0;
    while (e < -pow(2, nbexpo-1))
    {
        e   = e+1;
        sh = sh+1;
    }
    e = e & ((int)(pow(2,nbexpo)-1));
    e = e << nbmant;

    // mantissa ---------------------------------------------------------------

    if (nbmant == 23)
    {
        if (ifl & 0x00000001) m = m+1; // arredonda
    }
    else
    {
        sh = 23-nbmant+sh;
        int carry = (m >> (sh-1)) & 0x00000001; // carry de arredondamento
        m = m >> sh;
        if (carry) m = m+1; // arredonda
    }
    return s + e + m;
}

int main(void)
{
    char a[] = "-10";

    int nbmant = 20;
    int nbexpo = 5;

    int b = f2mf(a, nbmant, nbexpo);
    printf("%x", b);
}