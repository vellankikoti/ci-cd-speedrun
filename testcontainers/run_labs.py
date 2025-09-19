#!/usr/bin/env python3
"""
TestContainers Lab Runner
=========================

Simple runner for cleaned up TestContainers labs.
"""

import os
import sys
import subprocess

def run_lab(lab_path):
    """Run a specific lab"""
    print(f"\n🚀 Running {lab_path}")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, lab_path], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run {lab_path}: {e}")
        return False

def main():
    """Main lab runner"""
    print("🧪 TestContainers Lab Runner")
    print("=" * 40)
    
    # Available labs
    labs = {
        "1": "labs/basics/lab1_first_container.py",
        "2": "labs/basics/lab2_database_connection.py", 
        "3": "labs/basics/lab3_data_management.py",
        "4": "labs/basics/lab4_multiple_containers.py",
        "5": "labs/intermediate/lab5_multi_database.py",
        "6": "labs/intermediate/lab6_api_testing.py",
        "8": "labs/advanced/lab8_advanced_patterns.py",
        "examples": "quick_examples.py"
    }
    
    print("Available labs:")
    for key, path in labs.items():
        print(f"  {key}: {path}")
    
    print("\nOptions:")
    print("  all     - Run all labs")
    print("  basics  - Run basic labs (1-4)")
    print("  intermediate - Run intermediate labs (5-6)")
    print("  advanced - Run advanced labs (8)")
    print("  examples - Run quick examples")
    print("  <number> - Run specific lab")
    
    choice = input("\nEnter your choice: ").strip().lower()
    
    if choice == "all":
        print("\n🔄 Running all labs...")
        for key, path in labs.items():
            if key.isdigit():
                run_lab(path)
    elif choice == "basics":
        print("\n🔄 Running basic labs...")
        for i in range(1, 5):
            run_lab(labs[str(i)])
    elif choice == "intermediate":
        print("\n🔄 Running intermediate labs...")
        for i in range(5, 7):
            run_lab(labs[str(i)])
    elif choice == "advanced":
        print("\n🔄 Running advanced labs...")
        run_lab(labs["8"])
    elif choice == "examples":
        run_lab(labs["examples"])
    elif choice in labs:
        run_lab(labs[choice])
    else:
        print(f"❌ Unknown choice: {choice}")
        return False
    
    print("\n✅ Lab runner completed!")
    return True

if __name__ == "__main__":
    main()
