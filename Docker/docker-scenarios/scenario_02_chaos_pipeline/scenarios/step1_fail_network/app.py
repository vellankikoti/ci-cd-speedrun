import sys
import socket

print("STEP 1: NETWORK FAILURE")
print("=" * 30)
print("Trying to connect to nonexistent host...")

try:
    s = socket.create_connection(("nonexistent-host-12345.com", 80), timeout=3)
    print("Unexpected: Network is working!")
    s.close()
    sys.exit(1)
except Exception as e:
    print(f"Network error as expected: {e}")
    print("This step is supposed to fail due to network issues.")
    sys.exit(1)
