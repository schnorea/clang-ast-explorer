#include <iostream>
#include <vector>
#include <string>

// This is a comment block that should be highlighted
// when you select the comment AST node

namespace MyNamespace {
    
    class ComplexClass {
    private:
        std::string name;
        int value;
        
    public:
        // Constructor with initializer list
        ComplexClass(const std::string& n, int v) 
            : name(n), value(v) {
            std::cout << "Created: " << name << std::endl;
        }
        
        // Method with complex body
        void processData() {
            if (value > 0) {
                for (int i = 0; i < value; ++i) {
                    std::cout << "Processing item " << i 
                              << " for " << name << std::endl;
                }
            } else {
                std::cout << "No processing needed for " 
                          << name << std::endl;
            }
        }
        
        // Getter method
        const std::string& getName() const { 
            return name; 
        }
    };
    
    // Template function
    template<typename T>
    T findMaximum(const std::vector<T>& vec) {
        if (vec.empty()) {
            throw std::runtime_error("Empty vector");
        }
        
        T max_val = vec[0];
        for (const auto& item : vec) {
            if (item > max_val) {
                max_val = item;
            }
        }
        return max_val;
    }
}

int main() {
    // Create objects to test extent highlighting
    MyNamespace::ComplexClass obj1("Object1", 3);
    MyNamespace::ComplexClass obj2("Object2", 0);
    
    // Test method calls
    obj1.processData();
    obj2.processData();
    
    // Test template function
    std::vector<int> numbers = {1, 5, 3, 9, 2};
    try {
        int max_num = MyNamespace::findMaximum(numbers);
        std::cout << "Maximum number: " << max_num << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}