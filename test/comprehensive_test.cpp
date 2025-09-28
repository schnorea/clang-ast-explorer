#include <iostream>
#include <vector>
#include <string>

// Macro definition to generate MACRO_DEFINITION cursor
#define MAX_SIZE 100
#define SQUARE(x) ((x) * (x))

// Typedef to generate TYPEDEF_DECL cursor  
typedef int MyInteger;
typedef std::vector<int> IntVector;

// Enum to generate ENUM_DECL and ENUM_CONSTANT_DECL cursors
enum Color {
    RED,
    GREEN, 
    BLUE
};

enum class Status : int {
    ACTIVE = 1,
    INACTIVE = 0,
    PENDING = 2
};

// Struct to generate STRUCT_DECL cursor
struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}
};

struct Rectangle {
    Point topLeft;
    Point bottomRight;
    
    double area() const {
        return (bottomRight.x - topLeft.x) * (bottomRight.y - topLeft.y);
    }
};

// Union for additional variety
union Value {
    int intVal;
    float floatVal;
    char charVal;
};

// Class with destructor to generate DESTRUCTOR cursor
class ResourceManager {
private:
    int* data;
    size_t size;
    
public:
    // Constructor (already generates CONSTRUCTOR)
    ResourceManager(size_t s) : size(s) {
        data = new int[size];
        for (size_t i = 0; i < size; ++i) {
            data[i] = 0;
        }
    }
    
    // Copy constructor
    ResourceManager(const ResourceManager& other) : size(other.size) {
        data = new int[size];
        for (size_t i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }
    
    // Destructor to generate DESTRUCTOR cursor
    ~ResourceManager() {
        delete[] data;
        data = nullptr;
    }
    
    // Assignment operator
    ResourceManager& operator=(const ResourceManager& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            for (size_t i = 0; i < size; ++i) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }
    
    // Method to access data
    int& operator[](size_t index) {
        return data[index];
    }
    
    const int& operator[](size_t index) const {
        return data[index];
    }
    
    size_t getSize() const { return size; }
};

// Namespace to generate NAMESPACE_DECL cursor
namespace Graphics {
    struct Pixel {
        unsigned char r, g, b, a;
    };
    
    class Image {
    private:
        Pixel* pixels;
        int width, height;
        
    public:
        Image(int w, int h) : width(w), height(h) {
            pixels = new Pixel[width * height];
        }
        
        ~Image() {
            delete[] pixels;
        }
        
        Pixel& getPixel(int x, int y) {
            return pixels[y * width + x];
        }
    };
}

// Template class to generate more template cursors
template<typename T, int N>
class StaticArray {
private:
    T data[N];
    
public:
    StaticArray() {
        for (int i = 0; i < N; ++i) {
            data[i] = T{};
        }
    }
    
    T& operator[](int index) {
        return data[index];
    }
    
    const T& operator[](int index) const {
        return data[index];
    }
    
    constexpr int size() const {
        return N;
    }
};

// Function with various control flow to generate missing statement cursors
void controlFlowDemo(int value) {
    // Switch statement to generate SWITCH_STMT, CASE_STMT, DEFAULT_STMT
    switch (value) {
        case 1:
            std::cout << "One" << std::endl;
            break; // BREAK_STMT
        case 2:
        case 3:
            std::cout << "Two or Three" << std::endl;
            break;
        default: // DEFAULT_STMT
            std::cout << "Other" << std::endl;
            break;
    }
    
    // Do-while loop to generate DO_STMT
    int counter = 0;
    do {
        counter++;
        if (counter > 10) {
            break; // BREAK_STMT in loop
        }
        if (counter % 2 == 0) {
            continue; // CONTINUE_STMT
        }
        std::cout << counter << " ";
    } while (counter < 5);
    
    // Goto and label to generate GOTO_STMT and LABEL_STMT
    if (value < 0) {
        goto error_handler; // GOTO_STMT
    }
    
    std::cout << "Normal execution" << std::endl;
    return;
    
error_handler: // LABEL_STMT
    std::cout << "Error: negative value" << std::endl;
    
    ; // NULL_STMT (empty statement)
}

// Function demonstrating various expressions
void expressionDemo() {
    int arr[10] = {1, 2, 3, 4, 5}; // INIT_LIST_EXPR
    
    // Various literals
    int integer = 42; // INTEGER_LITERAL
    double floating = 3.14; // FLOATING_LITERAL  
    char character = 'A'; // CHARACTER_LITERAL
    const char* string = "Hello World"; // STRING_LITERAL
    bool boolean = true; // CXX_BOOL_LITERAL_EXPR
    
    int* ptr = nullptr; // CXX_NULL_PTR_LITERAL_EXPR
    
    // Dynamic allocation
    int* dynamic = new int(100); // CXX_NEW_EXPR
    delete dynamic; // CXX_DELETE_EXPR
    
    // Array access
    int value = arr[3]; // ARRAY_SUBSCRIPT_EXPR
    
    // Compound assignments
    value += 10; // COMPOUND_ASSIGNMENT_OPERATOR
    value *= 2;
    value /= 3;
    
    // Conditional operator
    int result = (value > 50) ? 100 : 0; // CONDITIONAL_OPERATOR
    
    // Parenthesized expressions
    int calc = ((value + 5) * 2); // PAREN_EXPR
    
    // Type casting
    double converted = static_cast<double>(value); // CAST_EXPR
}

// Template function to generate FUNCTION_TEMPLATE cursor
template<typename T>
T maximum(const T& a, const T& b) {
    return (a > b) ? a : b;
}

// Function with exception handling
void exceptionDemo() {
    try { // CXX_TRY_STMT
        throw std::runtime_error("Test exception");
    } catch (const std::exception& e) { // CXX_CATCH_STMT
        std::cout << "Caught exception: " << e.what() << std::endl;
    }
}

int main() {
    // Use various features to generate diverse AST
    MyInteger num = 42;
    Color favoriteColor = RED;
    Status currentStatus = Status::ACTIVE;
    
    Point p1(1.0, 2.0);
    Rectangle rect{Point(0, 0), Point(10, 5)};
    
    Value val;
    val.intVal = 123;
    
    ResourceManager manager(MAX_SIZE);
    manager[0] = SQUARE(5);
    
    Graphics::Image img(800, 600);
    Graphics::Pixel& pixel = img.getPixel(100, 200);
    
    StaticArray<int, 10> staticArr;
    staticArr[0] = maximum(10, 20);
    
    controlFlowDemo(2);
    expressionDemo();
    exceptionDemo();
    
    return 0;
}