import sys
import sqlalchemy

print("STEP 4: DATABASE FAILURE")
print("=" * 30)
print("Trying to connect to MySQL...")

try:
    engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost:3306/test')
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    print("Unexpected: MySQL is running!")
    sys.exit(1)
except Exception as e:
    print(f"Database error as expected: {e}")
    print("This step is supposed to fail due to missing database.")
    sys.exit(1)
