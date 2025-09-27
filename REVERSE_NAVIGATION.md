# Reverse Navigation Feature

## Overview

The AST Explorer now supports **bidirectional navigation** between source code and AST structure:

- **Forward Navigation** (existing): Click AST node → highlights source code extent
- **Reverse Navigation** (new): Click source code line → selects corresponding AST node

## How It Works

### User Experience
1. **Open a C++ file** in the AST Explorer
2. **Hover over source code lines** to see hover highlighting that indicates clickable areas
3. **Notice the cursor changes** to a hand pointer over clickable lines
4. **Click on any line** in the Source Code viewer
5. **Watch the AST Structure** automatically unfold and visually select the most specific node
6. **See node details** updated in the Node Information panel
7. **Status bar feedback** shows what type of AST node was found

### Technical Implementation

#### Click Detection
- Click events are captured on the source code text widget
- Mouse coordinates are converted to line/column positions
- Line number prefixes ("nnnn: ") are automatically accounted for

#### Node Finding Algorithm
The `find_node_at_location(line, column)` method:

1. **Traverses the AST tree** starting from the root
2. **Checks each node's extent** to see if it contains the target location
3. **Recursively searches children** to find the most specific match
4. **Returns the deepest node** that contains the clicked location

```python
def find_node_at_location(self, line: int, column: int) -> Optional[ASTNode]:
    """Find the most specific AST node that contains the given location"""
    
    def node_contains_location(node: ASTNode, target_line: int, target_col: int) -> bool:
        # Check if node's extent contains the target location
        extent = node.cursor.extent
        # ... bounds checking logic ...
        
    def find_most_specific(node: ASTNode, target_line: int, target_col: int) -> Optional[ASTNode]:
        # Recursively find the most specific containing node
        # ... recursive search logic ...
```

#### Tree Navigation
The `select_and_reveal_node(target_node)` method:

1. **Gets the path** to the target node from root (list of child indices)
2. **Follows the path** in the tree widget, expanding parents as needed
3. **Selects and scrolls** to make the target node visible
4. **Triggers selection events** to ensure proper visual highlighting
5. **Updates UI panels** with node information

#### Visual Feedback
Enhanced user experience with:

1. **Hover highlighting** - Lines glow when mouse hovers over them
2. **Cursor changes** - Hand pointer indicates clickable areas  
3. **Line highlighting** - Subtle background color shows current hover line
4. **Automatic cleanup** - Hover effects clear when mouse leaves the area

## Examples

### Function Declaration
```cpp
int main() {  // <- Click here
    return 0;
}
```
**Result**: Selects `FUNCTION_DECL` node for `main`

### Variable Declaration
```cpp
int main() {
    int x = 42;  // <- Click on 'int' or 'x'
    return 0;
}
```
**Result**: Selects `VAR_DECL` node for `x`

### Expression
```cpp
int main() {
    return 42;  // <- Click on '42'
}
```
**Result**: Selects `INTEGER_LITERAL` node for `42`

### Complex Structure
```cpp
class MyClass {
public:
    void method() {  // <- Click anywhere in method signature
        // ...
    }
};
```
**Result**: Selects `CXX_METHOD` node for `method`

## Benefits

### For Learning
- **Immediate feedback** on how C++ constructs map to AST nodes
- **Visual understanding** of AST structure and nesting
- **Exploration-friendly** - just click to discover

### For Development
- **Quick navigation** from source code issues to AST analysis
- **Debugging aid** for understanding parser behavior
- **Code analysis** workflow improvement

### For Research
- **Interactive exploration** of language constructs
- **Pattern recognition** in AST structures
- **Efficient investigation** of specific code locations

## Limitations

- **Accuracy depends on clang parsing** - some template errors may affect results
- **File boundaries** - only works within the currently loaded file
- **Extent availability** - some nodes may not have complete extent information
- **Click precision** - clicking between tokens may select parent nodes

## Error Handling

The feature includes robust error handling:

- **Graceful degradation** when nodes can't be found
- **Status bar feedback** for user awareness
- **Exception handling** prevents crashes from parsing issues
- **Fallback behavior** when extent information is unavailable

## Future Enhancements

Potential improvements for future versions:

- **Multi-file navigation** - handle includes and cross-file references
- **Token-level precision** - select exact tokens rather than just lines
- **Context menu integration** - right-click options for advanced navigation
- **History tracking** - remember previous navigation actions
- **Keyboard shortcuts** - hotkeys for common navigation patterns

## Testing

Use the provided test utility to verify functionality:

```bash
cd testers/
python test_reverse_navigation.py
```

This tests the backend logic for finding nodes at specific locations without requiring the full GUI.