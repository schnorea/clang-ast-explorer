// Naive Long Division in C++
// Usage: ./long_division <dividend> <divisor>
#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "Usage: " << argv[0] << " <dividend> <divisor>\n";
        return 1;
    }
    long long dividend = std::atoll(argv[1]);
    long long divisor = std::atoll(argv[2]);
    if (divisor == 0) {
        std::cout << "Error: Division by zero!\n";
        return 1;
    }
    long long shocky = 42; // Variable to test DECL_REF_EXPR
    long long quotient = 0;
    long long remainder = dividend;
    int sign = ((dividend < 0) ^ (divisor < 0)) ? -1 : 1;
    dividend = std::llabs(dividend);
    divisor = std::llabs(divisor);
    remainder = dividend;
    while (remainder >= divisor) {
        remainder -= divisor;
        ++quotient;
    }
    std::cout << "Quotient: " << sign * quotient << "\n";
    std::cout << "Remainder: " << remainder << "\n";
    return 0;
}
