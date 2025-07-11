import sys

print("STEP 2: RESOURCE FAILURE")
print("=" * 30)
print("Trying to allocate 2GB of memory...")

try:
    x = ' ' * (1024 * 1024 * 1024 * 2)  # 2GB allocation
    print("Unexpected: Allocation succeeded!")
    sys.exit(1)
except MemoryError as e:
    print(f"MemoryError as expected: {e}")
    print("This step is supposed to fail due to resource limits.")
    sys.exit(1)
