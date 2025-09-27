# File Monitoring Feature

## Overview
The AST Explorer now includes automatic file monitoring that detects when the currently loaded C++ file is modified externally and offers to reload the updated version.

## How It Works

### 1. Automatic Monitoring
- When you load a C++ file, monitoring starts automatically
- The system checks the file's modification time every 1 second
- Monitoring runs in the background without affecting performance

### 2. Change Detection
- **File Modified**: Shows dialog asking if you want to reload
- **File Deleted**: Shows warning and stops monitoring
- **File Moved**: Detected as deletion, stops monitoring

### 3. User Options
When a file change is detected, you get a dialog with options:
- **Yes**: Reload and re-parse the file automatically
- **No**: Continue with the current version (ignore changes)

## Features

### Automatic Updates
- **AST Tree**: Rebuilt with new parsing results
- **Source Code View**: Updated with new file content
- **Node Information**: Cleared and ready for new selections
- **Status Bar**: Shows monitoring status and file changes

### Menu Controls
- **File → Reload Current File**: Manual reload option
- **Tools → Auto-Monitor File Changes**: Toggle monitoring on/off

### Smart Handling
- **Error Recovery**: If reload fails, keeps current version
- **File Validation**: Checks file exists before monitoring
- **Resource Management**: Automatically stops monitoring when appropriate

## Use Cases

### 1. External Editor Workflow
1. Load a C++ file in AST Explorer
2. Edit the file in VS Code, Vim, or your preferred editor
3. Save the changes
4. AST Explorer automatically detects changes and asks to reload
5. Choose "Yes" to see updated AST structure immediately

### 2. Build System Integration
- Monitor generated C++ files that change during builds
- Automatically see AST changes from preprocessor modifications
- Track template instantiations and macro expansions

### 3. Collaborative Development
- See changes made by other developers in real-time
- Monitor files in shared development environments
- Track version control updates to files

## Technical Details

### Monitoring Method
- Uses `os.path.getmtime()` to check file modification times
- Polling interval: 1000ms (1 second)
- **Dialog Debouncing**: Prevents multiple dialogs for same change
- **Smart Detection**: Only triggers on significant time changes (>0.1s)
- Lightweight implementation with minimal system impact

### File Operations
- **Detection**: Modification time comparison
- **Validation**: File existence and accessibility checks  
- **Recovery**: Graceful handling of file system errors

### UI Integration
- **Non-blocking**: Monitoring runs in background
- **User Control**: Can be enabled/disabled via menu
- **Status Updates**: Clear feedback about monitoring state

## Testing the Feature

### 1. Manual Testing
1. Open AST Explorer and load `test/monitor_test.cpp`
2. Edit the file in another editor (add comments, modify code)
3. Save the file
4. Watch for the reload dialog in AST Explorer

### 2. Automated Demo
```bash
# Run the file monitoring demo script
python file_monitor_demo.py test/monitor_test.cpp 3

# This will modify the file every 3 seconds
# Watch AST Explorer for change notifications
```

### 3. Dialog Debouncing Test
```bash
# Test rapid file changes (should show only ONE dialog)
python rapid_test.py test/monitor_test.cpp 5

# Makes 5 rapid changes in 0.5 seconds
# Should trigger only one reload dialog
```

### 3. Menu Testing
- Use **Tools → Auto-Monitor File Changes** to toggle monitoring
- Use **File → Reload Current File** for manual reloads
- Check status bar for monitoring feedback

## Benefits

### 1. Improved Workflow
- No need to manually reload files after external edits
- Seamless integration with external editors
- Real-time AST exploration during development

### 2. Better Productivity  
- Immediate feedback on code changes
- Quick iteration cycle for AST analysis
- Reduced manual file management

### 3. Enhanced Collaboration
- See team changes reflected immediately
- Monitor build-generated files automatically
- Track version control updates in real-time

## Configuration

### Default Settings
- **Monitoring**: Enabled by default for all loaded files
- **Check Interval**: 1000ms (1 second)
- **Auto-reload**: User choice via dialog (no automatic reload)

### Customization
- Check interval can be modified in code (`file_check_interval`)
- Monitoring can be disabled via Tools menu
- Dialog behavior is user-controlled (always asks before reloading)

## Error Handling

### File System Errors
- **File Deleted**: Shows warning, stops monitoring
- **Permission Errors**: Graceful degradation with error messages
- **Network Files**: Works with network-mounted files

### Parse Errors
- **Syntax Errors**: Shows error dialog, keeps previous version
- **Template Issues**: Offers relaxed parsing as fallback
- **Recovery**: Always maintains stable state

This feature makes the AST Explorer much more convenient for real-world development workflows!