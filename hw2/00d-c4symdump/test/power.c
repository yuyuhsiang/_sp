#include <stdio.h>
int power(int n){
    if (n == 0) return 1;
    return 2 * power(n - 1);
}
int main() {
    printf("power(3)=%d\n", power(3));
}