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
- `TYPEDEF_DECL` - Typedef declarations

### Statements
- `COMPOUND_STMT` - Block statements `{}`
- `IF_STMT` - If statements
- `FOR_STMT` - For loops
- `WHILE_STMT` - While loops
- `RETURN_STMT` - Return statements

### Expressions
- `BINARY_OPERATOR` - Binary operations (+, -, *, etc.)
- `UNARY_OPERATOR` - Unary operations (++, --, !, etc.)
- `CALL_EXPR` - Function calls
- `DECL_REF_EXPR` - References to declared entities
- `INTEGER_LITERAL` - Integer constants
- `STRING_LITERAL` - String constants

### References
- `TYPE_REF` - References to types
- `TEMPLATE_REF` - Template references

## Integration with EnergyPlus Analysis

For EnergyPlus dependency analysis, key cursor properties to focus on:

1. **Data Dependencies**: `VAR_DECL`, `DECL_REF_EXPR` cursors to track variable usage
2. **Control Dependencies**: `IF_STMT`, `FOR_STMT`, `WHILE_STMT` for control flow
3. **Compute Dependencies**: `CALL_EXPR` for function calls and computational dependencies
4. **Memory Dependencies**: `get_field_offsetof()` for data structure layout analysis

This comprehensive cursor interface enables sophisticated static analysis of C++ code for understanding dependencies, control flow, and computational patterns in complex software like EnergyPlus.
