#include <stdio.h>
#include <stdlib.h>


int f2mf(char *va)
{
    float f = atof(va);

    int ifl = (int)&f;

    return ifl;
}

int main(void)
{
    char a[] = "10";

    int b = f2mf(a);
    printf("%x", b);

    return 0;
}   