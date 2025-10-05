#!/usr/bin/env python3
"""
Lab 8: Advanced Patterns - Chaos Scenarios
==========================================

Experience advanced chaos in production environments.
Learn how to handle complex failures, data corruption, and system breakdowns.
"""

import os
import sys
import time
import threading
import random
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
        # Check if docker command exists
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        
        # Check if Docker daemon is running
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        
        # If docker ps fails, try docker info as fallback
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
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

def chaos_data_corruption():
    """Data corruption chaos - what happens when data gets corrupted?"""
    print("\n💥 Data Corruption Chaos...")
    print("🚨 What happens when data gets corrupted in production?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            
            # Setup database
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE critical_data (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    balance DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Critical Data Table Created")
            
            # Insert critical data
            critical_records = [
                (1001, 1500.00, "active"),
                (1002, 2500.00, "active"),
                (1003, 750.00, "suspended"),
                (1004, 3000.00, "active")
            ]
            
            print("📝 Creating Critical Data:")
            for user_id, balance, status in critical_records:
                cursor.execute(
                    "INSERT INTO critical_data (user_id, balance, status) VALUES (%s, %s, %s)",
                    (user_id, balance, status)
                )
                print(f"   + User {user_id}: ${balance} ({status})")
            
            conn.commit()
            
            # Simulate data corruption scenarios
            print(f"\n🧪 Simulating Data Corruption:")
            
            # Scenario 1: Balance corruption
            print(f"\n   Scenario 1: Balance Corruption")
            cursor.execute("UPDATE critical_data SET balance = -999999.99 WHERE user_id = 1001")
            conn.commit()
            print(f"      💥 User 1001 balance corrupted to -$999,999.99")
            
            # Scenario 2: Status corruption
            print(f"\n   Scenario 2: Status Corruption")
            cursor.execute("UPDATE critical_data SET status = 'INVALID_STATUS' WHERE user_id = 1002")
            conn.commit()
            print(f"      💥 User 1002 status corrupted to 'INVALID_STATUS'")
            
            # Scenario 3: Data type corruption
            print(f"\n   Scenario 3: Data Type Corruption")
            cursor.execute("UPDATE critical_data SET user_id = 'NOT_A_NUMBER' WHERE user_id = 1003")
            conn.commit()
            print(f"      💥 User 1003 ID corrupted to 'NOT_A_NUMBER'")
            
            # Show corrupted data
            print(f"\n📊 Corrupted Data State:")
            cursor.execute("SELECT user_id, balance, status FROM critical_data ORDER BY id")
            corrupted_data = cursor.fetchall()
            
            for user_id, balance, status in corrupted_data:
                print(f"   User {user_id}: ${balance} ({status})")
            
            # Test data validation
            print(f"\n🔍 Data Validation Test:")
            try:
                cursor.execute("SELECT SUM(balance) FROM critical_data")
                total_balance = cursor.fetchone()[0]
                print(f"   Total Balance: ${total_balance}")
            except Exception as e:
                print(f"   ❌ Data validation failed: {str(e)[:50]}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Data corruption test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement data validation and integrity checks!")

def chaos_system_breakdown():
    """System breakdown chaos - what happens when systems fail completely?"""
    print("\n💥 System Breakdown Chaos...")
    print("🚨 What happens when critical systems fail completely?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup systems
            conn = psycopg2.connect(
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
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE system_status (
                    id SERIAL PRIMARY KEY,
                    service_name VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 System Status Table Created")
            
            # Initialize system status
            services = ["database", "cache", "api", "queue", "monitoring"]
            for service in services:
                cursor.execute(
                    "INSERT INTO system_status (service_name, status) VALUES (%s, %s)",
                    (service, "healthy")
                )
                print(f"   + {service}: healthy")
            
            conn.commit()
            
            # Simulate system breakdown
            print(f"\n🧪 Simulating System Breakdown:")
            
            # Scenario 1: Database failure
            print(f"\n   Scenario 1: Database Failure")
            cursor.execute("UPDATE system_status SET status = 'failed' WHERE service_name = 'database'")
            conn.commit()
            print(f"      💥 Database: FAILED")
            
            # Try to use database
            try:
                cursor.execute("SELECT 1")
                print(f"      ❌ Database still accessible (unexpected)")
            except Exception as e:
                print(f"      ✅ Database properly failed: {str(e)[:50]}")
            
            # Scenario 2: Cache failure
            print(f"\n   Scenario 2: Cache Failure")
            cursor.execute("UPDATE system_status SET status = 'failed' WHERE service_name = 'cache'")
            conn.commit()
            print(f"      💥 Cache: FAILED")
            
            # Try to use cache
            try:
                r.ping()
                print(f"      ❌ Cache still accessible (unexpected)")
            except Exception as e:
                print(f"      ✅ Cache properly failed: {str(e)[:50]}")
            
            # Scenario 3: Cascading failure
            print(f"\n   Scenario 3: Cascading Failure")
            cursor.execute("UPDATE system_status SET status = 'failed' WHERE service_name IN ('api', 'queue', 'monitoring')")
            conn.commit()
            print(f"      💥 API: FAILED")
            print(f"      💥 Queue: FAILED")
            print(f"      💥 Monitoring: FAILED")
            
            # Show system status
            print(f"\n📊 System Status After Breakdown:")
            cursor.execute("SELECT service_name, status FROM system_status ORDER BY service_name")
            system_status = cursor.fetchall()
            
            for service, status in system_status:
                status_icon = "❌" if status == "failed" else "✅"
                print(f"   {status_icon} {service}: {status}")
            
            # Calculate system health
            healthy_services = len([s for s in system_status if s[1] == "healthy"])
            total_services = len(system_status)
            health_percentage = (healthy_services / total_services) * 100
            
            print(f"\n🏥 System Health: {healthy_services}/{total_services} services healthy ({health_percentage:.1f}%)")
            
            if health_percentage < 50:
                print(f"   🚨 CRITICAL: System is in critical state!")
            elif health_percentage < 80:
                print(f"   ⚠️  WARNING: System is degraded!")
            else:
                print(f"   ✅ System is healthy!")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 System breakdown test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement circuit breakers and graceful degradation!")

def chaos_resource_exhaustion():
    """Resource exhaustion chaos - what happens when resources run out?"""
    print("\n💥 Resource Exhaustion Chaos...")
    print("🚨 What happens when system resources are exhausted?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup systems
            conn = psycopg2.connect(
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
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE resource_usage (
                    id SERIAL PRIMARY KEY,
                    resource_type VARCHAR(50) NOT NULL,
                    usage_percentage DECIMAL(5,2) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Resource Usage Table Created")
            
            # Simulate resource exhaustion
            print(f"\n🧪 Simulating Resource Exhaustion:")
            
            # Scenario 1: Memory exhaustion
            print(f"\n   Scenario 1: Memory Exhaustion")
            memory_levels = [45.2, 67.8, 89.3, 95.7, 99.1]
            
            for level in memory_levels:
                cursor.execute(
                    "INSERT INTO resource_usage (resource_type, usage_percentage) VALUES (%s, %s)",
                    ("memory", level)
                )
                print(f"      📊 Memory usage: {level}%")
                
                if level > 90:
                    print(f"      ⚠️  WARNING: Memory usage critical!")
                elif level > 80:
                    print(f"      ⚠️  CAUTION: Memory usage high!")
            
            # Scenario 2: CPU exhaustion
            print(f"\n   Scenario 2: CPU Exhaustion")
            cpu_levels = [35.1, 58.4, 82.6, 96.2, 99.8]
            
            for level in cpu_levels:
                cursor.execute(
                    "INSERT INTO resource_usage (resource_type, usage_percentage) VALUES (%s, %s)",
                    ("cpu", level)
                )
                print(f"      📊 CPU usage: {level}%")
                
                if level > 95:
                    print(f"      🚨 CRITICAL: CPU usage critical!")
                elif level > 80:
                    print(f"      ⚠️  WARNING: CPU usage high!")
            
            # Scenario 3: Disk space exhaustion
            print(f"\n   Scenario 3: Disk Space Exhaustion")
            disk_levels = [42.3, 68.9, 87.4, 94.6, 98.9]
            
            for level in disk_levels:
                cursor.execute(
                    "INSERT INTO resource_usage (resource_type, usage_percentage) VALUES (%s, %s)",
                    ("disk", level)
                )
                print(f"      📊 Disk usage: {level}%")
                
                if level > 95:
                    print(f"      🚨 CRITICAL: Disk space critical!")
                elif level > 85:
                    print(f"      ⚠️  WARNING: Disk space low!")
            
            conn.commit()
            
            # Analyze resource exhaustion
            print(f"\n📊 Resource Exhaustion Analysis:")
            
            cursor.execute("""
                SELECT resource_type, 
                       MAX(usage_percentage) as max_usage,
                       AVG(usage_percentage) as avg_usage,
                       COUNT(*) as measurements
                FROM resource_usage
                GROUP BY resource_type
                ORDER BY max_usage DESC
            """)
            
            resource_analysis = cursor.fetchall()
            for resource, max_usage, avg_usage, measurements in resource_analysis:
                print(f"   {resource.upper()}:")
                print(f"      Max Usage: {max_usage}%")
                print(f"      Avg Usage: {avg_usage:.1f}%")
                print(f"      Measurements: {measurements}")
                
                if max_usage > 95:
                    print(f"      🚨 CRITICAL: Resource exhausted!")
                elif max_usage > 80:
                    print(f"      ⚠️  WARNING: Resource under pressure!")
                else:
                    print(f"      ✅ Resource healthy!")
            
            # Test system behavior under resource pressure
            print(f"\n🧪 Testing System Behavior Under Resource Pressure:")
            
            # Try to perform operations under high resource usage
            try:
                cursor.execute("SELECT COUNT(*) FROM resource_usage")
                count = cursor.fetchone()[0]
                print(f"   📊 Database query successful: {count} records")
            except Exception as e:
                print(f"   ❌ Database query failed: {str(e)[:50]}")
            
            try:
                r.ping()
                print(f"   📊 Cache ping successful")
            except Exception as e:
                print(f"   ❌ Cache ping failed: {str(e)[:50]}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Resource exhaustion test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement resource monitoring and auto-scaling!")

def chaos_network_partitions():
    """Network partition chaos - what happens when networks are partitioned?"""
    print("\n💥 Network Partition Chaos...")
    print("🚨 What happens when network connectivity is lost?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup systems
            conn = psycopg2.connect(
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
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE network_events (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    source VARCHAR(50) NOT NULL,
                    target VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Network Events Table Created")
            
            # Simulate network partitions
            print(f"\n🧪 Simulating Network Partitions:")
            
            # Scenario 1: Database partition
            print(f"\n   Scenario 1: Database Partition")
            cursor.execute("""
                INSERT INTO network_events (event_type, source, target, status)
                VALUES ('connection_lost', 'api_service', 'database', 'failed')
            """)
            print(f"      💥 API Service lost connection to Database")
            
            # Scenario 2: Cache partition
            print(f"\n   Scenario 2: Cache Partition")
            cursor.execute("""
                INSERT INTO network_events (event_type, source, target, status)
                VALUES ('connection_lost', 'api_service', 'cache', 'failed')
            """)
            print(f"      💥 API Service lost connection to Cache")
            
            # Scenario 3: Service-to-service partition
            print(f"\n   Scenario 3: Service-to-Service Partition")
            cursor.execute("""
                INSERT INTO network_events (event_type, source, target, status)
                VALUES ('connection_lost', 'user_service', 'order_service', 'failed')
            """)
            print(f"      💥 User Service lost connection to Order Service")
            
            # Scenario 4: Partial network recovery
            print(f"\n   Scenario 4: Partial Network Recovery")
            cursor.execute("""
                INSERT INTO network_events (event_type, source, target, status)
                VALUES ('connection_restored', 'api_service', 'database', 'success')
            """)
            print(f"      ✅ API Service restored connection to Database")
            
            conn.commit()
            
            # Analyze network partition impact
            print(f"\n📊 Network Partition Analysis:")
            
            cursor.execute("""
                SELECT event_type, COUNT(*) as count
                FROM network_events
                GROUP BY event_type
                ORDER BY count DESC
            """)
            
            event_summary = cursor.fetchall()
            print(f"   📈 Network Events Summary:")
            for event_type, count in event_summary:
                print(f"      {event_type}: {count} events")
            
            # Test connectivity after partitions
            print(f"\n🔍 Testing Connectivity After Partitions:")
            
            # Test database connectivity
            try:
                cursor.execute("SELECT 1")
                cursor.fetchone()
                print(f"   ✅ Database: Connected")
            except Exception as e:
                print(f"   ❌ Database: Connection failed - {str(e)[:50]}")
            
            # Test cache connectivity
            try:
                r.ping()
                print(f"   ✅ Cache: Connected")
            except Exception as e:
                print(f"   ❌ Cache: Connection failed - {str(e)[:50]}")
            
            # Show network status
            print(f"\n📊 Network Status:")
            cursor.execute("""
                SELECT source, target, status, COUNT(*) as event_count
                FROM network_events
                GROUP BY source, target, status
                ORDER BY source, target
            """)
            
            network_status = cursor.fetchall()
            for source, target, status, count in network_status:
                status_icon = "✅" if status == "success" else "❌"
                print(f"   {status_icon} {source} -> {target}: {status} ({count} events)")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Network partition test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement network resilience and failover mechanisms!")

def main():
    """Run Advanced Patterns Chaos Scenarios"""
    print("💥 LAB 8: ADVANCED PATTERNS CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world advanced resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_data_corruption()
        chaos_system_breakdown()
        chaos_resource_exhaustion()
        chaos_network_partitions()
        
        print("\n🎉 ADVANCED PATTERNS CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Data corruption happens - implement validation and integrity checks")
        print("• System breakdowns occur - implement circuit breakers and graceful degradation")
        print("• Resource exhaustion is real - implement monitoring and auto-scaling")
        print("• Network partitions happen - implement resilience and failover mechanisms")
        print("• Real-world advanced failures are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for advanced production chaos!")
        
    except Exception as e:
        print(f"❌ Advanced patterns chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
