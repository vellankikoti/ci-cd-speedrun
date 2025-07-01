import os
import sys
import pytest

def main():
    mode = os.environ.get("SCENARIO_4_PASS", "true").lower() == "true"
    if mode:
        print("=== Running Secret Scan PASS Test ===")
        result = pytest.main(["test_secret_scan_pass.py", "--maxfail=1", "--disable-warnings"])
    else:
        print("=== Running Secret Scan FAIL Test ===")
        result = pytest.main(["test_secret_scan_fail.py", "--maxfail=1", "--disable-warnings"])
    sys.exit(result)

if __name__ == "__main__":
    main()