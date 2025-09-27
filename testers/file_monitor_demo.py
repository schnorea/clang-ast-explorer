#!/usr/bin/env python3
"""
File Monitoring Demo - Test script to demonstrate external file modification
"""

import time
import sys
import os

def modify_test_file(filename="../test/extent_test.cpp", interval=5):
    """Modify a test file periodically to test file monitoring"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return
    
    print(f"File Monitoring Demo")
    print(f"===================")
    print(f"This script will modify '{filename}' every {interval} seconds.")
    print(f"Watch the AST Explorer to see file change notifications.")
    print(f"Press Ctrl+C to stop.\n")
    
    counter = 0
    
    try:
        while True:
            counter += 1
            
            # Read current file content
            with open(filename, 'r') as f:
                content = f.read()
            
            # Add a comment at the end
            timestamp = time.strftime("%H:%M:%S")
            new_comment = f"\n// Auto-generated comment #{counter} at {timestamp}\n"
            
            # Write back with new comment
            with open(filename, 'w') as f:
                f.write(content + new_comment)
            
            print(f"[{timestamp}] Modified {filename} (change #{counter})")
            print(f"  Added: {new_comment.strip()}")
            print(f"  Next change in {interval} seconds...\n")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\nDemo stopped. Modified {filename} {counter} times.")
        
        # Clean up - remove auto-generated comments
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Remove auto-generated comments
            clean_lines = []
            for line in lines:
                if "Auto-generated comment" not in line:
                    clean_lines.append(line)
            
            with open(filename, 'w') as f:
                f.writelines(clean_lines)
                
            print(f"Cleaned up {filename}")
            
        except Exception as e:
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    # Allow specifying file and interval as command line arguments
    filename = sys.argv[1] if len(sys.argv) > 1 else "test/extent_test.cpp"
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    modify_test_file(filename, interval)