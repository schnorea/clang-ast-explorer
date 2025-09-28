# Clang Python Bindings - Translation Unit Cursor Analysis

## Overview

This document describes the properties and methods available on a Clang cursor object when analyzing C/C++ source code using the Python bindings for libclang. The cursor represents a node in the Abstract Syntax Tree (AST) and provides comprehensive information about code elements.

## Translation Unit Structure

When parsing a C/C++ file using `clang.cindex`, you get a translation unit with a root cursor that contains the entire AST. Each cursor in the tree represents a different language construct (variables, functions, statements, etc.).

## Cursor Attributes and Methods

### Core Object Properties
- `__buffer__` - Internal buffer representation
- `__class__` - Python class type information  
- `__dict__` - Object's namespace dictionary
- `__module__` - Module where the class is defined
- `_b_base_`, `_b_needsfree_` - Internal ctypes management
- `_fields_` - Internal structure field definitions
- `_kind_id` - Internal kind identifier
- `_objects` - Internal object references
- `_spelling` - Internal cached spelling
- `_tu` - Reference to translation unit

### Identification and Classification
- **`kind`** - The cursor kind (e.g., `VAR_DECL`, `FUNCTION_DECL`, `IF_STMT`)
- **`spelling`** - The name/identifier of the cursor (variable name, function name, etc.)
- **`displayname`** - Human-readable display name
- **`usr`** - Unified Symbol Resolution identifier (unique across translation units)
- **`hash`** - Hash value for the cursor

### Location and Extent
- **`location`** - Source location (file, line, column) where cursor is defined
- **`extent`** - Source range (start and end locations) that the cursor spans
- **`translation_unit`** - Reference to the containing translation unit

### Type Information  
- **`type`** - The type of the cursor (e.g., `int`, `void`, custom types)
- **`result_type`** - Return type for functions
- **`enum_type`** - Type information for enum cursors
- **`enum_value`** - Value for enum constant cursors
- **`underlying_typedef_type`** - Underlying type for typedef cursors

### Hierarchy and Relationships
- **`semantic_parent`** - Semantic parent in the AST hierarchy
- **`lexical_parent`** - Lexical parent (where defined in source)
- **`canonical`** - Canonical cursor (resolves through typedefs, etc.)
- **`referenced`** - The cursor that this cursor references
- **`get_definition()`** - Get the definition cursor for declarations

### Navigation and Traversal
- **`get_children()`** - Iterator over direct child cursors
- **`walk_preorder()`** - Preorder traversal of the subtree
- **`get_tokens()`** - Get all tokens within the cursor's extent

### Function/Method Analysis
- **`get_arguments()`** - Function parameter cursors
- **`get_num_template_arguments()`** - Number of template arguments
- **`get_template_argument_kind()`** - Template argument type information
- **`get_template_argument_type()`** - Template argument types
- **`get_template_argument_value()`** - Template argument values
- **`get_template_argument_unsigned_value()`** - Unsigned template values

### Method/Class Properties
- **`is_const_method()`** - Whether method is const
- **`is_static_method()`** - Whether method is static
- **`is_virtual_method()`** - Whether method is virtual
- **`is_pure_virtual_method()`** - Whether method is pure virtual
- **`is_default_method()`** - Whether method is defaulted
- **`is_deleted_method()`** - Whether method is deleted
- **`is_explicit_method()`** - Whether constructor is explicit
- **`is_converting_constructor()`** - Whether constructor is converting
- **`is_copy_constructor()`** - Whether it's a copy constructor
- **`is_move_constructor()`** - Whether it's a move constructor
- **`is_default_constructor()`** - Whether it's a default constructor
- **`is_copy_assignment_operator_method()`** - Copy assignment operator
- **`is_move_assignment_operator_method()`** - Move assignment operator

### Record/Class Analysis
- **`is_abstract_record()`** - Whether class is abstract
- **`is_anonymous()`** - Whether entity is anonymous
- **`is_anonymous_record_decl()`** - Whether record is anonymous
- **`is_definition()`** - Whether cursor is a definition (not just declaration)

### Field and Memory Layout
- **`is_bitfield()`** - Whether field is a bitfield
- **`is_mutable_field()`** - Whether field is mutable
- **`get_bitfield_width()`** - Width of bitfield in bits
- **`get_field_offsetof()`** - Offset of field within struct
- **`get_base_offsetof()`** - Offset of base class

### Enum Analysis
- **`is_scoped_enum()`** - Whether enum is scoped (enum class)

### Inheritance
- **`is_virtual_base()`** - Whether base class is virtual

### Storage and Linkage
- **`storage_class`** - Storage class (static, extern, etc.)
- **`linkage`** - Linkage type (internal, external, etc.)
- **`tls_kind`** - Thread-local storage information

### Documentation and Comments
- **`brief_comment`** - Brief documentation comment
- **`raw_comment`** - Raw comment text
- **`pretty_printed`** - Pretty-printed representation

### Accessibility
- **`access_specifier`** - Access level (public, private, protected)

### Availability and Platform
- **`availability`** - Platform availability information

### Advanced Features
- **`binary_operator`** - Binary operator information
- **`exception_specification_kind`** - Exception specification type
- **`objc_type_encoding`** - Objective-C type encoding
- **`mangled_name`** - Mangled symbol name

### File Inclusion
- **`get_included_file()`** - File included by include directive

### Utility Methods
- **`from_cursor_result()`** - Create cursor from result
- **`from_location()`** - Create cursor from location  
- **`from_result()`** - Create cursor from libclang result

## Common Usage Patterns

### Basic AST Traversal
```python
def visit_node(cursor, indent=0):
    print(f"{' ' * indent}{cursor.kind}: {cursor.spelling}")
    for child in cursor.get_children():
        visit_node(child, indent + 2)

# Start traversal from translation unit root
visit_node(translation_unit.cursor)
```

### Finding Specific Node Types
```python
def find_functions(cursor):
    functions = []
    if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        functions.append(cursor)
    
    for child in cursor.get_children():
        functions.extend(find_functions(child))
    
    return functions
```

### Analyzing Function Signatures
```python
def analyze_function(cursor):
    if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        print(f"Function: {cursor.spelling}")
        print(f"Return type: {cursor.result_type.spelling}")
        print("Parameters:")
        for arg in cursor.get_arguments():
            print(f"  {arg.type.spelling} {arg.spelling}")
```

### Dependency Analysis
```python
def find_variable_dependencies(cursor):
    dependencies = []
    
    if cursor.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        # Variable reference
        dependencies.append(cursor.spelling)
    elif cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
        # Function call
        dependencies.append(cursor.spelling)
    
    for child in cursor.get_children():
        dependencies.extend(find_variable_dependencies(child))
    
    return dependencies
```

## Cursor Kinds Reference

### Declarations
- `FUNCTION_DECL` - Function declarations
- `VAR_DECL` - Variable declarations  
- `PARM_DECL` - Parameter declarations
- `STRUCT_DECL` - Struct declarations
- `CLASS_DECL` - Class declarations
- `ENUM_DECL` - Enum declarations
- `ENUM_CONSTANT_DECL` - Enum constant declarations
- `TYPEDEF_DECL` - Typedef declarations
- `NAMESPACE_DECL` - Namespace declarations
- `FIELD_DECL` - Class/struct member field declarations
- `CXX_METHOD` - C++ class method declarations
- `CONSTRUCTOR` - Constructor declarations
- `DESTRUCTOR` - Destructor declarations
- `CONVERSION_FUNCTION` - Type conversion function declarations
- `TEMPLATE_TYPE_PARAMETER` - Template type parameter declarations
- `TEMPLATE_NON_TYPE_PARAMETER` - Template non-type parameter declarations

### Statements
- `COMPOUND_STMT` - Block statements `{}`
- `DECL_STMT` - Declaration statements (variable declarations within functions)
- `IF_STMT` - If statements
- `FOR_STMT` - For loops
- `WHILE_STMT` - While loops
- `DO_STMT` - Do-while loops
- `SWITCH_STMT` - Switch statements
- `CASE_STMT` - Case labels in switch statements
- `DEFAULT_STMT` - Default labels in switch statements
- `BREAK_STMT` - Break statements
- `CONTINUE_STMT` - Continue statements
- `GOTO_STMT` - Goto statements
- `LABEL_STMT` - Label statements
- `NULL_STMT` - Empty statements (just semicolon)
- `RETURN_STMT` - Return statements

### Expressions
- `BINARY_OPERATOR` - Binary operations (+, -, *, etc.)
- `UNARY_OPERATOR` - Unary operations (++, --, !, etc.)
- `CONDITIONAL_OPERATOR` - Ternary operator (? :)
- `CALL_EXPR` - Function calls
- `MEMBER_REF_EXPR` - Member access (obj.member)
- `ARRAY_SUBSCRIPT_EXPR` - Array subscript (arr[index])
- `CAST_EXPR` - Type casting expressions
- `COMPOUND_ASSIGNMENT_OPERATOR` - Compound assignments (+=, -=, etc.)
- `DECL_REF_EXPR` - References to declared entities
- `PAREN_EXPR` - Parenthesized expressions
- `INIT_LIST_EXPR` - Initialization list expressions {1, 2, 3}
- `INTEGER_LITERAL` - Integer constants
- `FLOATING_LITERAL` - Floating-point constants
- `CHARACTER_LITERAL` - Character constants ('a')
- `STRING_LITERAL` - String constants ("hello")
- `CXX_BOOL_LITERAL_EXPR` - Boolean literals (true/false)
- `CXX_NULL_PTR_LITERAL_EXPR` - nullptr literal
- `CXX_THIS_EXPR` - 'this' pointer expression
- `CXX_NEW_EXPR` - new expressions
- `CXX_DELETE_EXPR` - delete expressions

### References
- `TYPE_REF` - References to types
- `TEMPLATE_REF` - Template references
- `NAMESPACE_REF` - References to namespaces
- `MEMBER_REF` - References to class members
- `LABEL_REF` - References to labels
- `OVERLOADED_DECL_REF` - References to overloaded declarations

### Preprocessing
- `MACRO_DEFINITION` - Macro definitions (#define)
- `MACRO_INSTANTIATION` - Macro usage/expansion
- `INCLUSION_DIRECTIVE` - Include directives (#include)

### Templates
- `CLASS_TEMPLATE` - Class template declarations
- `FUNCTION_TEMPLATE` - Function template declarations
- `CLASS_TEMPLATE_PARTIAL_SPECIALIZATION` - Partial template specializations
- `TEMPLATE_TEMPLATE_PARAMETER` - Template template parameters

### Other Common Cursors
- `TRANSLATION_UNIT` - Root of the AST (entire file)
- `UNEXPOSED_EXPR` - Expressions not yet handled by libclang
- `UNEXPOSED_STMT` - Statements not yet handled by libclang
- `UNEXPOSED_DECL` - Declarations not yet handled by libclang
- `UNEXPOSED_ATTR` - Attributes not yet handled by libclang

## Integration with EnergyPlus Analysis

For EnergyPlus dependency analysis, key cursor properties to focus on:

1. **Data Dependencies**: `VAR_DECL`, `DECL_REF_EXPR` cursors to track variable usage
2. **Control Dependencies**: `IF_STMT`, `FOR_STMT`, `WHILE_STMT` for control flow
3. **Compute Dependencies**: `CALL_EXPR` for function calls and computational dependencies
4. **Memory Dependencies**: `get_field_offsetof()` for data structure layout analysis

This comprehensive cursor interface enables sophisticated static analysis of C++ code for understanding dependencies, control flow, and computational patterns in complex software like EnergyPlus.
