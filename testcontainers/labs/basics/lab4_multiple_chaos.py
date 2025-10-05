#!/usr/bin/env python3
"""
Lab 4: Multiple Containers - Chaos Scenarios
============================================

Experience multi-container chaos in production environments.
Learn how to handle container failures, network issues, and orchestration problems.
"""

import os
import sys
import time
import threading
from pathlib import Path

# Python version check
if sys.version_info < (3, 10):
    print("❌ Python 3.10 or higher is required")
    sys.exit(1)

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

# Platform-specific Docker host configuration
if sys.platform == "win32":
    os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
else:
    os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'testcontainers': 'testcontainers',
        'psycopg2': 'psycopg2-binary',
        'redis': 'redis'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_docker():
    """Check if Docker is available and running"""
    import subprocess
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis")
    sys.exit(1)

def chaos_container_failures():
    """Container failure chaos - what happens when containers fail?"""
    print("\n💥 Container Failure Chaos...")
    print("🚨 What happens when one container fails in a multi-container setup?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup initial data
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            pg_cursor = pg_conn.cursor()
            pg_cursor.execute("""
                CREATE TABLE critical_data (
                    id SERIAL PRIMARY KEY,
                    data VARCHAR(100) NOT NULL,
                    processed BOOLEAN DEFAULT false,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Critical Data Table Created")

            # Insert critical data
            critical_data = [
                "Transaction #001 - $1000.00",
                "Transaction #002 - $2500.00",
                "Transaction #003 - $500.00",
                "Transaction #004 - $1500.00"
            ]

            print("📝 Inserting Critical Data:")
            for data in critical_data:
                pg_cursor.execute(
                    "INSERT INTO critical_data (data) VALUES (%s)",
                    (data,)
                )
                print(f"   + {data}")

            pg_conn.commit()

            # Store processing status in Redis
            print("📝 Storing Processing Status in Redis:")
            for i, data in enumerate(critical_data, 1):
                r.hset(f"processing:{i}", mapping={
                    "data": data,
                    "status": "pending",
                    "attempts": "0",
                    "last_attempt": str(int(time.time()))
                })
                print(f"   🔑 Processing {i}: {data} (pending)")

            # Simulate processing failures
            print(f"\n🧪 Simulating Processing Failures:")
            
            processing_results = []
            
            for i, data in enumerate(critical_data, 1):
                try:
                    # Simulate processing attempt
                    print(f"   🔄 Processing {data}...")
                    
                    # Simulate random failures
                    import random
                    if random.random() < 0.3:  # 30% failure rate
                        raise Exception("Processing timeout - service unavailable")
                    
                    # Mark as processed in database
                    pg_cursor.execute(
                        "UPDATE critical_data SET processed = true WHERE id = %s",
                        (i,)
                    )
                    
                    # Update Redis status
                    r.hset(f"processing:{i}", mapping={
                        "status": "completed",
                        "attempts": "1",
                        "last_attempt": str(int(time.time()))
                    })
                    
                    processing_results.append(f"✅ {data}: Success")
                    print(f"      ✅ Success")
                    
                except Exception as e:
                    # Update Redis with failure
                    attempts = int(r.hget(f"processing:{i}", "attempts") or "0") + 1
                    r.hset(f"processing:{i}", mapping={
                        "status": "failed",
                        "attempts": str(attempts),
                        "last_attempt": str(int(time.time())),
                        "error": str(e)[:50]
                    })
                    
                    processing_results.append(f"❌ {data}: Failed - {str(e)[:30]}")
                    print(f"      ❌ Failed: {str(e)[:30]}")
                    
                    pg_conn.rollback()

            # Show final processing status
            print(f"\n📊 Final Processing Status:")
            for result in processing_results:
                print(f"   {result}")

            # Show database state
            pg_cursor.execute("SELECT COUNT(*) FROM critical_data WHERE processed = true")
            processed_count = pg_cursor.fetchone()[0]
            pg_cursor.execute("SELECT COUNT(*) FROM critical_data")
            total_count = pg_cursor.fetchone()[0]

            print(f"\n📊 Database State:")
            print(f"   Processed: {processed_count}/{total_count} records")
            print(f"   Success Rate: {(processed_count/total_count)*100:.1f}%")

            # Show Redis state
            print(f"\n📊 Redis State:")
            for i in range(1, len(critical_data) + 1):
                status = r.hget(f"processing:{i}", "status")
                attempts = r.hget(f"processing:{i}", "attempts")
                print(f"   Processing {i}: {status} (attempts: {attempts})")

            pg_cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Container failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement retry logic and circuit breakers for container failures!")

def chaos_network_partitions():
    """Network partition chaos - what happens when containers can't communicate?"""
    print("\n💥 Network Partition Chaos...")
    print("🚨 What happens when containers lose network connectivity?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup distributed system
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            pg_cursor = pg_conn.cursor()
            pg_cursor.execute("""
                CREATE TABLE distributed_data (
                    id SERIAL PRIMARY KEY,
                    key_name VARCHAR(100) UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Distributed Data Table Created")

            # Insert initial data
            initial_data = [
                ("user:1001", "Alice Johnson"),
                ("user:1002", "Bob Smith"),
                ("user:1003", "Carol Davis")
            ]

            print("📝 Creating Initial Data:")
            for key_name, value in initial_data:
                pg_cursor.execute(
                    "INSERT INTO distributed_data (key_name, value) VALUES (%s, %s)",
                    (key_name, value)
                )
                print(f"   + {key_name}: {value}")

            pg_conn.commit()

            # Store in Redis cache
            print("📝 Caching Data in Redis:")
            for key_name, value in initial_data:
                r.set(f"cache:{key_name}", value, ex=300)  # 5 minutes TTL
                print(f"   💾 {key_name}: {value} (TTL: 300s)")

            # Simulate network partition scenarios
            print(f"\n🧪 Simulating Network Partition Scenarios:")

            # Scenario 1: Database becomes unreachable
            print(f"\n   Scenario 1: Database Unreachable")
            try:
                # Simulate database connection failure
                pg_cursor.execute("SELECT 1")
                print("   ✅ Database connection: OK")
            except Exception as e:
                print(f"   ❌ Database connection: FAILED - {str(e)[:30]}")

            # Scenario 2: Redis becomes unreachable
            print(f"\n   Scenario 2: Redis Unreachable")
            try:
                r.ping()
                print("   ✅ Redis connection: OK")
            except Exception as e:
                print(f"   ❌ Redis connection: FAILED - {str(e)[:30]}")

            # Scenario 3: Data inconsistency due to partition
            print(f"\n   Scenario 3: Data Inconsistency")
            
            # Update data in database (simulating one partition)
            pg_cursor.execute("UPDATE distributed_data SET value = 'Alice Johnson (Updated)', version = version + 1 WHERE key_name = 'user:1001'")
            pg_conn.commit()
            print("   📝 Database updated: user:1001 -> Alice Johnson (Updated)")

            # Update data in Redis (simulating another partition)
            r.set("cache:user:1001", "Alice Johnson (Cached Update)", ex=300)
            print("   💾 Redis updated: user:1001 -> Alice Johnson (Cached Update)")

            # Check for data inconsistency
            pg_cursor.execute("SELECT value FROM distributed_data WHERE key_name = 'user:1001'")
            db_value = pg_cursor.fetchone()[0]
            redis_value = r.get("cache:user:1001")

            print(f"   📊 Data Consistency Check:")
            print(f"      Database: {db_value}")
            print(f"      Redis: {redis_value}")
            print(f"      Consistent: {'✅' if db_value == redis_value else '❌'}")

            # Scenario 4: Split-brain scenario
            print(f"\n   Scenario 4: Split-Brain Scenario")
            
            # Simulate conflicting updates
            pg_cursor.execute("UPDATE distributed_data SET value = 'Alice Johnson (DB Update)', version = version + 1 WHERE key_name = 'user:1002'")
            pg_conn.commit()
            
            r.set("cache:user:1002", "Alice Johnson (Cache Update)", ex=300)
            
            print("   📝 Conflicting updates applied:")
            print("      Database: Alice Johnson (DB Update)")
            print("      Redis: Alice Johnson (Cache Update)")
            print("   ⚠️  Split-brain detected - manual resolution required!")

            pg_cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Network partition test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement conflict resolution and data synchronization strategies!")

def chaos_resource_exhaustion():
    """Resource exhaustion chaos - what happens when containers run out of resources?"""
    print("\n💥 Resource Exhaustion Chaos...")
    print("🚨 What happens when containers run out of memory, CPU, or disk space?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup monitoring
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            # Monitor initial resource usage
            print("📊 Initial Resource Usage:")
            
            # PostgreSQL stats
            pg_cursor = pg_conn.cursor()
            pg_cursor.execute("SELECT pg_database_size(current_database())")
            db_size = pg_cursor.fetchone()[0]
            print(f"   🐘 PostgreSQL DB Size: {db_size / 1024:.1f} KB")

            # Redis stats
            redis_info = r.info()
            print(f"   🔴 Redis Memory: {redis_info['used_memory_human']}")
            print(f"   🔴 Redis Keys: {r.dbsize()}")

            # Simulate memory exhaustion in Redis
            print(f"\n🧪 Simulating Redis Memory Exhaustion:")
            
            large_data = "x" * 1024  # 1KB string
            successful_sets = 0
            failed_sets = 0
            
            for i in range(1000):  # Try to set 1000 keys
                try:
                    key = f"large_data:{i}"
                    r.set(key, large_data, ex=60)  # 1 minute TTL
                    successful_sets += 1
                    
                    if i % 100 == 0:
                        redis_info = r.info()
                        print(f"   📊 Set {i} keys: {redis_info['used_memory_human']} used")
                        
                except redis.exceptions.ResponseError as e:
                    if "OOM" in str(e):
                        failed_sets += 1
                        print(f"   ❌ Out of Memory at key {i}: {str(e)[:50]}")
                        break
                    else:
                        raise

            print(f"\n📊 Memory Exhaustion Results:")
            print(f"   Successful sets: {successful_sets}")
            print(f"   Failed sets: {failed_sets}")
            print(f"   Success rate: {(successful_sets/(successful_sets+failed_sets))*100:.1f}%")

            # Simulate database disk space exhaustion
            print(f"\n🧪 Simulating Database Disk Space Issues:")
            
            # Create large table
            pg_cursor.execute("""
                CREATE TABLE large_data (
                    id SERIAL PRIMARY KEY,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("   📊 Large Data Table Created")

            # Insert large amounts of data
            large_text = "x" * 1000  # 1KB per row
            successful_inserts = 0
            failed_inserts = 0

            for i in range(1000):  # Try to insert 1000 rows
                try:
                    pg_cursor.execute(
                        "INSERT INTO large_data (data) VALUES (%s)",
                        (large_text,)
                    )
                    successful_inserts += 1
                    
                    if i % 100 == 0:
                        pg_cursor.execute("SELECT pg_database_size(current_database())")
                        current_size = pg_cursor.fetchone()[0]
                        print(f"   📊 Inserted {i} rows: {current_size / 1024:.1f} KB")
                        
                except Exception as e:
                    if "disk" in str(e).lower() or "space" in str(e).lower():
                        failed_inserts += 1
                        print(f"   ❌ Disk space error at row {i}: {str(e)[:50]}")
                        break
                    else:
                        raise

            pg_conn.commit()

            print(f"\n📊 Disk Space Results:")
            print(f"   Successful inserts: {successful_inserts}")
            print(f"   Failed inserts: {failed_inserts}")
            print(f"   Success rate: {(successful_inserts/(successful_inserts+failed_inserts))*100:.1f}%")

            # Show final resource usage
            pg_cursor.execute("SELECT pg_database_size(current_database())")
            final_db_size = pg_cursor.fetchone()[0]
            final_redis_info = r.info()

            print(f"\n📊 Final Resource Usage:")
            print(f"   🐘 PostgreSQL DB Size: {final_db_size / 1024:.1f} KB")
            print(f"   🔴 Redis Memory: {final_redis_info['used_memory_human']}")
            print(f"   🔴 Redis Keys: {r.dbsize()}")

            pg_cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Resource exhaustion test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Monitor resource usage and implement proper limits!")

def chaos_orchestration_failures():
    """Orchestration failure chaos - what happens when container orchestration fails?"""
    print("\n💥 Orchestration Failure Chaos...")
    print("🚨 What happens when container orchestration and coordination fails?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup distributed transaction system
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            pg_cursor = pg_conn.cursor()
            pg_cursor.execute("""
                CREATE TABLE distributed_transactions (
                    id SERIAL PRIMARY KEY,
                    transaction_id VARCHAR(100) UNIQUE NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    participants TEXT[],
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Distributed Transactions Table Created")

            # Simulate distributed transaction scenarios
            print(f"\n🧪 Simulating Distributed Transaction Failures:")

            # Scenario 1: Two-phase commit failure
            print(f"\n   Scenario 1: Two-Phase Commit Failure")
            
            transaction_id = "txn_001"
            participants = ["postgres", "redis", "external_service"]
            
            # Start transaction
            pg_cursor.execute("""
                INSERT INTO distributed_transactions (transaction_id, participants) 
                VALUES (%s, %s)
            """, (transaction_id, participants))
            pg_conn.commit()
            
            print(f"   📝 Started transaction: {transaction_id}")
            print(f"   👥 Participants: {', '.join(participants)}")

            # Phase 1: Prepare
            print(f"   🔄 Phase 1: Prepare")
            prepare_results = []
            
            for participant in participants:
                if participant == "postgres":
                    try:
                        pg_cursor.execute("SELECT 1")
                        prepare_results.append(f"✅ {participant}: Ready")
                    except Exception as e:
                        prepare_results.append(f"❌ {participant}: Failed - {str(e)[:30]}")
                        
                elif participant == "redis":
                    try:
                        r.ping()
                        prepare_results.append(f"✅ {participant}: Ready")
                    except Exception as e:
                        prepare_results.append(f"❌ {participant}: Failed - {str(e)[:30]}")
                        
                elif participant == "external_service":
                    # Simulate external service failure
                    prepare_results.append(f"❌ {participant}: Failed - Service unavailable")
            
            for result in prepare_results:
                print(f"      {result}")

            # Check if all participants are ready
            all_ready = all("✅" in result for result in prepare_results)
            
            if all_ready:
                print(f"   🔄 Phase 2: Commit")
                pg_cursor.execute("UPDATE distributed_transactions SET status = 'committed' WHERE transaction_id = %s", (transaction_id,))
                pg_conn.commit()
                print(f"   ✅ Transaction committed successfully")
            else:
                print(f"   🔄 Phase 2: Rollback")
                pg_cursor.execute("UPDATE distributed_transactions SET status = 'rolled_back' WHERE transaction_id = %s", (transaction_id,))
                pg_conn.commit()
                print(f"   ❌ Transaction rolled back due to participant failure")

            # Scenario 2: Split-brain in orchestration
            print(f"\n   Scenario 2: Split-Brain in Orchestration")
            
            # Simulate conflicting orchestration decisions
            print(f"   🧠 Orchestrator A: Start service X")
            print(f"   🧠 Orchestrator B: Stop service X")
            print(f"   ⚠️  Split-brain detected - conflicting orchestration decisions!")
            print(f"   🔧 Resolution: Manual intervention required")

            # Scenario 3: Cascading failures
            print(f"\n   Scenario 3: Cascading Failures")
            
            failure_chain = [
                "Database connection pool exhausted",
                "Application server overloaded",
                "Load balancer health check failures",
                "User requests timing out",
                "System-wide service degradation"
            ]
            
            print(f"   📉 Failure Chain:")
            for i, failure in enumerate(failure_chain, 1):
                print(f"      {i}. {failure}")
                if i < len(failure_chain):
                    time.sleep(0.2)  # Simulate delay between failures

            print(f"   💥 System-wide failure - all services affected!")

            # Show final transaction state
            pg_cursor.execute("SELECT transaction_id, status, participants FROM distributed_transactions")
            transactions = pg_cursor.fetchall()
            
            print(f"\n📊 Final Transaction State:")
            for txn_id, status, participants in transactions:
                status_icon = "✅" if status == "committed" else "❌" if status == "rolled_back" else "⏳"
                print(f"   {status_icon} {txn_id}: {status} ({', '.join(participants)})")

            pg_cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Orchestration failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement proper orchestration patterns and failure recovery!")

def main():
    """Run Multiple Container Chaos Scenarios"""
    print("💥 LAB 4: MULTIPLE CONTAINER CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world multi-container resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_container_failures()
        chaos_network_partitions()
        chaos_resource_exhaustion()
        chaos_orchestration_failures()
        
        print("\n🎉 MULTIPLE CONTAINER CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Container failures happen - implement retry logic and circuit breakers")
        print("• Network partitions occur - implement conflict resolution strategies")
        print("• Resource exhaustion is real - monitor usage and set proper limits")
        print("• Orchestration can fail - implement proper coordination patterns")
        print("• Real-world multi-container systems are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for multi-container production chaos!")
        
    except Exception as e:
        print(f"❌ Multiple container chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
