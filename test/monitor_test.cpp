#include <iostream>
#include <string>

// Simple test file for file monitoring
class TestClass {
private:
    std::string message;
    int value;
    
public:
    TestClass(const std::string& msg, int val) 
        : message(msg), value(val) {}
    
    void display() {
        std::cout << "Message: " << message 
                  << ", Value: " << value << std::endl;
    }
    
    int getValue() const { 
        return value; 
    }
};

int main() {
    TestClass test("Hello World", 42);
    test.display();
    
    std::cout << "Test value: " << test.getValue() << std::endl;
    
    return 0;
}