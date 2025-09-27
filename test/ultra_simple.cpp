// Ultra-simple C++ file that raw clang can handle
int x = 10;
int y = 20;

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(x, y);
    return result;
}