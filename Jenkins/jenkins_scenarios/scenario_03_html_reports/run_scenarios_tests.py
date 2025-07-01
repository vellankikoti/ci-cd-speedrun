#!/usr/bin/env python3
"""
CI/CD Chaos Workshop - Dynamic Test Runner
This script dynamically discovers and runs either pass or fail tests for a given scenario.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import glob

def find_test_files(test_dir, test_type):
    """
    Dynamically find test files based on the test type (pass or fail)
    
    Args:
        test_dir (str): Directory containing test files
        test_type (str): Either 'pass' or 'fail'
    
    Returns:
        list: List of test files matching the pattern
    """
    pattern = f"test_*_{test_type}.py"
    test_files = glob.glob(os.path.join(test_dir, pattern))
    
    if not test_files:
        print(f"⚠️ No test files found matching pattern: {pattern}")
        print(f"📁 Searching in directory: {test_dir}")
        
        # List all available test files for debugging
        all_test_files = glob.glob(os.path.join(test_dir, "test_*.py"))
        if all_test_files:
            print("📋 Available test files:")
            for file in all_test_files:
                print(f"   • {os.path.basename(file)}")
        else:
            print("❌ No test files found at all!")
    
    return test_files

def run_pytest_with_reports(test_files, output_dir, scenario_name):
    """
    Run pytest with HTML and JSON report generation
    
    Args:
        test_files (list): List of test files to run
        output_dir (str): Directory to save reports
        scenario_name (str): Name of the scenario for report naming
    
    Returns:
        int: Exit code from pytest
    """
    if not test_files:
        print("❌ No test files to run!")
        return 1
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Build pytest command
    html_report = os.path.join(output_dir, f"{scenario_name}_report.html")
    json_report = os.path.join(output_dir, f"{scenario_name}_report.json")
    
    pytest_cmd = [
        "pytest",
        *test_files,
        "--html", html_report,
        "--self-contained-html",
        "--json-report",
        "--json-report-file", json_report,
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    print(f"🧪 Running pytest command:")
    print(f"   {' '.join(pytest_cmd)}")
    print(f"📊 Reports will be saved to:")
    print(f"   • HTML: {html_report}")
    print(f"   • JSON: {json_report}")
    
    # Run pytest
    try:
        result = subprocess.run(pytest_cmd, capture_output=False)
        return result.returncode
    except FileNotFoundError:
        print("❌ Error: pytest not found. Make sure pytest is installed.")
        return 127
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return 1

def main():
    """Main function to handle command line arguments and run tests"""
    parser = argparse.ArgumentParser(
        description="CI/CD Chaos Workshop Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run passing tests for scenario 1
  python run_scenario_tests.py --scenario scenario_01_docker_build --type pass

  # Run failing tests for scenario 3
  python run_scenario_tests.py --scenario scenario_03_html_reports --type fail

  # Run tests with custom test directory
  python run_scenario_tests.py --scenario scenario_02_testcontainers --type pass --test-dir ./custom/tests
        """
    )
    
    parser.add_argument(
        "--scenario",
        required=True,
        help="Scenario name (e.g., scenario_01_docker_build)"
    )
    
    parser.add_argument(
        "--type",
        required=True,
        choices=["pass", "fail"],
        help="Test type to run: pass or fail"
    )
    
    parser.add_argument(
        "--test-dir",
        default="./tests",
        help="Directory containing test files (default: ./tests)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="./reports",
        help="Directory to save test reports (default: ./reports)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be run without actually running tests"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧪 CI/CD CHAOS WORKSHOP TEST RUNNER                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"🎯 Scenario: {args.scenario}")
    print(f"🔄 Test Type: {args.type.upper()}")
    print(f"📁 Test Directory: {args.test_dir}")
    print(f"📊 Output Directory: {args.output_dir}")
    
    # Validate test directory exists
    if not os.path.exists(args.test_dir):
        print(f"❌ Error: Test directory does not exist: {args.test_dir}")
        return 1
    
    # Find test files
    test_files = find_test_files(args.test_dir, args.type)
    
    if not test_files:
        print(f"❌ No {args.type} tests found for scenario {args.scenario}")
        return 1
    
    print(f"✅ Found {len(test_files)} test file(s):")
    for test_file in test_files:
        print(f"   • {os.path.basename(test_file)}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No tests will be executed")
        return 0
    
    # Run tests
    print(f"\n🚀 Running {args.type} tests for {args.scenario}...")
    exit_code = run_pytest_with_reports(test_files, args.output_dir, args.scenario)
    
    if exit_code == 0:
        print(f"\n✅ All {args.type} tests completed successfully!")
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")
        if args.type == "fail":
            print("💡 Note: If you ran 'fail' tests, failures are expected for learning purposes!")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())