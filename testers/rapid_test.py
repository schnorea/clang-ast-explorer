#!/usr/bin/env python3
"""
Quick File Touch Test - Creates rapid file modifications to test dialog debouncing
"""

import os
import time
import sys

def rapid_file_modifications(filename="../test/monitor_test.cpp", count=5):
    """Make rapid file modifications to test dialog debouncing"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return
    
    print(f"Rapid File Modification Test")
    print(f"===========================")
    print(f"Making {count} rapid modifications to '{filename}'")
    print(f"This should trigger only ONE dialog in the AST Explorer\n")
    
    # Read original content
    with open(filename, 'r') as f:
        original_content = f.read()
    
    for i in range(count):
        # Make small modification
        timestamp = time.strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
        comment = f"\n// Rapid modification #{i+1} at {timestamp}"
        
        with open(filename, 'w') as f:
            f.write(original_content + comment)
        
        print(f"Modification #{i+1} at {timestamp}")
        
        # Very short delay to create rapid changes
        time.sleep(0.1)
    
    print(f"\nCompleted {count} rapid modifications.")
    print("Check AST Explorer - you should see only ONE dialog!")
    
    # Wait a moment, then restore original
    time.sleep(2)
    
    with open(filename, 'w') as f:
        f.write(original_content)
    
    print(f"Restored original content of {filename}")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "test/monitor_test.cpp"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    rapid_file_modifications(filename, count)