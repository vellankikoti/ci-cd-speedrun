import sys
import redis

print("STEP 3: SERVICE FAILURE")
print("=" * 30)
print("Trying to connect to Redis...")

try:
    r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2)
    r.ping()
    print("Unexpected: Redis is running!")
    sys.exit(1)
except Exception as e:
    print(f"Service error as expected: {e}")
    print("This step is supposed to fail due to missing service.")
    sys.exit(1)
