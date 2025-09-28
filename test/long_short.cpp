// Naive Long Division in C++
// Usage: ./long_division <dividend> <divisor>
#include <iostream>
#include <cstdlib>

int main(void) {
    long long x = 5;
    long long y = 10;
    long long z = x + y; // 'x' and 'y' here are DECL_REF_EXPR

    if (x > 0) {      // A
        y = x + 1;    // B
        z = y * 2;    // C
    } else {
        y = x - 1;    // D
        z = y * 2;    // E
    }
}
