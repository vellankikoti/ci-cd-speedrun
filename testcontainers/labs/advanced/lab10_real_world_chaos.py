#!/usr/bin/env python3
"""
Lab 10: Real-World Scenarios - Chaos Scenarios
==============================================

Experience real-world chaos in production environments.
Learn how to handle complex failures, system breakdowns, and production disasters.
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

def chaos_production_disaster():
    """Production disaster chaos - what happens when everything fails?"""
    print("\n💥 Production Disaster Chaos...")
    print("🚨 What happens when multiple systems fail simultaneously?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup production systems
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
                CREATE TABLE disaster_log (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Disaster Log Table Created")
            
            # Simulate production disaster
            print(f"\n🧪 Simulating Production Disaster:")
            
            # Disaster scenario 1: Database corruption
            print(f"\n   Disaster 1: Database Corruption")
            cursor.execute("""
                INSERT INTO disaster_log (event_type, severity, message)
                VALUES ('database', 'CRITICAL', 'Database corruption detected in production')
            """)
            print(f"      💥 Database corruption detected!")
            
            # Disaster scenario 2: Cache failure
            print(f"\n   Disaster 2: Cache Failure")
            cursor.execute("""
                INSERT INTO disaster_log (event_type, severity, message)
                VALUES ('cache', 'CRITICAL', 'Redis cluster completely down')
            """)
            print(f"      💥 Redis cluster completely down!")
            
            # Disaster scenario 3: Network partition
            print(f"\n   Disaster 3: Network Partition")
            cursor.execute("""
                INSERT INTO disaster_log (event_type, severity, message)
                VALUES ('network', 'CRITICAL', 'Network partition isolating data center')
            """)
            print(f"      💥 Network partition isolating data center!")
            
            # Disaster scenario 4: Security breach
            print(f"\n   Disaster 4: Security Breach")
            cursor.execute("""
                INSERT INTO disaster_log (event_type, severity, message)
                VALUES ('security', 'CRITICAL', 'Unauthorized access detected in production')
            """)
            print(f"      💥 Security breach detected!")
            
            # Disaster scenario 5: Data loss
            print(f"\n   Disaster 5: Data Loss")
            cursor.execute("""
                INSERT INTO disaster_log (event_type, severity, message)
                VALUES ('data', 'CRITICAL', 'Critical data loss in production database')
            """)
            print(f"      💥 Critical data loss detected!")
            
            conn.commit()
            
            # Analyze disaster impact
            print(f"\n📊 Disaster Impact Analysis:")
            
            cursor.execute("""
                SELECT event_type, severity, COUNT(*) as count
                FROM disaster_log
                GROUP BY event_type, severity
                ORDER BY severity, count DESC
            """)
            
            disaster_analysis = cursor.fetchall()
            for event_type, severity, count in disaster_analysis:
                severity_icon = "🚨" if severity == "CRITICAL" else "⚠️"
                print(f"   {severity_icon} {event_type}: {count} {severity} events")
            
            # Test system behavior during disaster
            print(f"\n🧪 Testing System Behavior During Disaster:")
            
            # Test database operations
            try:
                cursor.execute("SELECT 1")
                cursor.fetchone()
                print(f"   ✅ Database: Still operational")
            except Exception as e:
                print(f"   ❌ Database: Failed - {str(e)[:50]}")
            
            # Test cache operations
            try:
                r.ping()
                print(f"   ✅ Cache: Still operational")
            except Exception as e:
                print(f"   ❌ Cache: Failed - {str(e)[:50]}")
            
            # Test data integrity
            try:
                cursor.execute("SELECT COUNT(*) FROM disaster_log")
                count = cursor.fetchone()[0]
                print(f"   ✅ Data Integrity: {count} disaster events logged")
            except Exception as e:
                print(f"   ❌ Data Integrity: Failed - {str(e)[:50]}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Production disaster test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement disaster recovery and business continuity plans!")

def chaos_cascading_failures():
    """Cascading failure chaos - what happens when failures cascade through systems?"""
    print("\n💥 Cascading Failure Chaos...")
    print("🚨 What happens when failures cascade through multiple systems?")
    
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
                CREATE TABLE cascade_log (
                    id SERIAL PRIMARY KEY,
                    service_name VARCHAR(50) NOT NULL,
                    failure_reason VARCHAR(100) NOT NULL,
                    affected_services TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Cascade Log Table Created")
            
            # Simulate cascading failures
            print(f"\n🧪 Simulating Cascading Failures:")
            
            # Failure chain
            failure_chain = [
                ("database", "Connection timeout", "user-service, order-service, payment-service"),
                ("user-service", "Database unavailable", "order-service, notification-service"),
                ("order-service", "User service unavailable", "payment-service, shipping-service"),
                ("payment-service", "Order service unavailable", "billing-service, audit-service"),
                ("notification-service", "User service unavailable", "email-service, sms-service"),
                ("shipping-service", "Order service unavailable", "logistics-service, tracking-service")
            ]
            
            for i, (service, reason, affected) in enumerate(failure_chain, 1):
                cursor.execute("""
                    INSERT INTO cascade_log (service_name, failure_reason, affected_services)
                    VALUES (%s, %s, %s)
                """, (service, reason, affected))
                
                print(f"   {i}. 💥 {service}: {reason}")
                print(f"      Affects: {affected}")
                
                # Simulate delay between failures
                time.sleep(0.1)
            
            conn.commit()
            
            # Analyze cascade impact
            print(f"\n📊 Cascade Impact Analysis:")
            
            cursor.execute("""
                SELECT service_name, 
                       COUNT(*) as failure_count,
                       STRING_AGG(affected_services, ', ') as all_affected
                FROM cascade_log
                GROUP BY service_name
                ORDER BY failure_count DESC
            """)
            
            cascade_analysis = cursor.fetchall()
            for service, failure_count, all_affected in cascade_analysis:
                print(f"   {service}:")
                print(f"      Failures: {failure_count}")
                print(f"      Affected Services: {all_affected}")
            
            # Calculate system health
            total_services = len(failure_chain)
            failed_services = len(set([f[0] for f in failure_chain]))
            health_percentage = ((total_services - failed_services) / total_services) * 100
            
            print(f"\n🏥 System Health: {health_percentage:.1f}% healthy")
            
            if health_percentage < 20:
                print(f"   🚨 CRITICAL: System in complete failure state!")
            elif health_percentage < 50:
                print(f"   🚨 CRITICAL: System severely degraded!")
            elif health_percentage < 80:
                print(f"   ⚠️  WARNING: System partially degraded!")
            else:
                print(f"   ✅ System mostly healthy!")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Cascading failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement circuit breakers and bulkheads!")

def chaos_data_corruption():
    """Data corruption chaos - what happens when critical data gets corrupted?"""
    print("\n💥 Data Corruption Chaos...")
    print("🚨 What happens when critical production data gets corrupted?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            
            # Setup production database
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE production_data (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    account_balance DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    last_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Production Data Table Created")
            
            # Insert critical production data
            critical_data = [
                (1001, 15000.00, "active"),
                (1002, 25000.00, "active"),
                (1003, 5000.00, "suspended"),
                (1004, 100000.00, "active"),
                (1005, 7500.00, "active")
            ]
            
            print("📝 Creating Critical Production Data:")
            for user_id, balance, status in critical_data:
                cursor.execute(
                    "INSERT INTO production_data (user_id, account_balance, status) VALUES (%s, %s, %s)",
                    (user_id, balance, status)
                )
                print(f"   + User {user_id}: ${balance} ({status})")
            
            conn.commit()
            
            # Simulate data corruption scenarios
            print(f"\n🧪 Simulating Data Corruption:")
            
            # Corruption 1: Balance corruption
            print(f"\n   Corruption 1: Balance Corruption")
            cursor.execute("UPDATE production_data SET account_balance = -999999.99 WHERE user_id = 1001")
            conn.commit()
            print(f"      💥 User 1001 balance corrupted to -$999,999.99")
            
            # Corruption 2: Status corruption
            print(f"\n   Corruption 2: Status Corruption")
            cursor.execute("UPDATE production_data SET status = 'CORRUPTED' WHERE user_id = 1002")
            conn.commit()
            print(f"      💥 User 1002 status corrupted to 'CORRUPTED'")
            
            # Corruption 3: Data type corruption
            print(f"\n   Corruption 3: Data Type Corruption")
            cursor.execute("UPDATE production_data SET user_id = 'INVALID' WHERE user_id = 1003")
            conn.commit()
            print(f"      💥 User 1003 ID corrupted to 'INVALID'")
            
            # Corruption 4: Timestamp corruption
            print(f"\n   Corruption 4: Timestamp Corruption")
            cursor.execute("UPDATE production_data SET last_transaction = 'INVALID_DATE' WHERE user_id = 1004")
            conn.commit()
            print(f"      💥 User 1004 timestamp corrupted to 'INVALID_DATE'")
            
            # Show corrupted data
            print(f"\n📊 Corrupted Data State:")
            cursor.execute("SELECT user_id, account_balance, status, last_transaction FROM production_data ORDER BY id")
            corrupted_data = cursor.fetchall()
            
            for user_id, balance, status, last_transaction in corrupted_data:
                print(f"   User {user_id}: ${balance} ({status}) - {last_transaction}")
            
            # Test data validation
            print(f"\n🔍 Data Validation Test:")
            
            # Test 1: Balance validation
            try:
                cursor.execute("SELECT SUM(account_balance) FROM production_data")
                total_balance = cursor.fetchone()[0]
                print(f"   Total Balance: ${total_balance}")
            except Exception as e:
                print(f"   ❌ Balance validation failed: {str(e)[:50]}")
            
            # Test 2: Status validation
            try:
                cursor.execute("SELECT COUNT(*) FROM production_data WHERE status = 'active'")
                active_count = cursor.fetchone()[0]
                print(f"   Active Accounts: {active_count}")
            except Exception as e:
                print(f"   ❌ Status validation failed: {str(e)[:50]}")
            
            # Test 3: Data type validation
            try:
                cursor.execute("SELECT COUNT(*) FROM production_data WHERE user_id > 0")
                valid_users = cursor.fetchone()[0]
                print(f"   Valid Users: {valid_users}")
            except Exception as e:
                print(f"   ❌ Data type validation failed: {str(e)[:50]}")
            
            # Test 4: Timestamp validation
            try:
                cursor.execute("SELECT COUNT(*) FROM production_data WHERE last_transaction > '2020-01-01'")
                valid_timestamps = cursor.fetchone()[0]
                print(f"   Valid Timestamps: {valid_timestamps}")
            except Exception as e:
                print(f"   ❌ Timestamp validation failed: {str(e)[:50]}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Data corruption test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement data validation and integrity checks!")

def chaos_security_breach():
    """Security breach chaos - what happens when security is compromised?"""
    print("\n💥 Security Breach Chaos...")
    print("🚨 What happens when security is compromised in production?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup security systems
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
                CREATE TABLE security_events (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    source_ip VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Security Events Table Created")
            
            # Simulate security breach scenarios
            print(f"\n🧪 Simulating Security Breach:")
            
            # Breach 1: Unauthorized access
            print(f"\n   Breach 1: Unauthorized Access")
            cursor.execute("""
                INSERT INTO security_events (event_type, severity, source_ip, description)
                VALUES ('unauthorized_access', 'CRITICAL', '192.168.1.100', 'Unauthorized access to production database')
            """)
            print(f"      💥 Unauthorized access from 192.168.1.100")
            
            # Breach 2: SQL injection attempt
            print(f"\n   Breach 2: SQL Injection Attempt")
            cursor.execute("""
                INSERT INTO security_events (event_type, severity, source_ip, description)
                VALUES ('sql_injection', 'HIGH', '10.0.0.50', 'SQL injection attempt detected in user input')
            """)
            print(f"      💥 SQL injection attempt from 10.0.0.50")
            
            # Breach 3: Brute force attack
            print(f"\n   Breach 3: Brute Force Attack")
            cursor.execute("""
                INSERT INTO security_events (event_type, severity, source_ip, description)
                VALUES ('brute_force', 'HIGH', '172.16.0.25', 'Multiple failed login attempts detected')
            """)
            print(f"      💥 Brute force attack from 172.16.0.25")
            
            # Breach 4: Data exfiltration
            print(f"\n   Breach 4: Data Exfiltration")
            cursor.execute("""
                INSERT INTO security_events (event_type, severity, source_ip, description)
                VALUES ('data_exfiltration', 'CRITICAL', '203.0.113.1', 'Large amount of data transferred to external IP')
            """)
            print(f"      💥 Data exfiltration to 203.0.113.1")
            
            # Breach 5: Privilege escalation
            print(f"\n   Breach 5: Privilege Escalation")
            cursor.execute("""
                INSERT INTO security_events (event_type, severity, source_ip, description)
                VALUES ('privilege_escalation', 'CRITICAL', '198.51.100.10', 'Unauthorized privilege escalation detected')
            """)
            print(f"      💥 Privilege escalation from 198.51.100.10")
            
            conn.commit()
            
            # Store security alerts in Redis
            print(f"\n💾 Storing Security Alerts in Redis:")
            
            cursor.execute("""
                SELECT event_type, severity, source_ip, description, timestamp
                FROM security_events
                ORDER BY timestamp DESC
            """)
            
            security_events = cursor.fetchall()
            for event_type, severity, source_ip, description, timestamp in security_events:
                alert_data = {
                    "event_type": event_type,
                    "severity": severity,
                    "source_ip": source_ip,
                    "description": description,
                    "timestamp": timestamp.isoformat()
                }
                r.setex(f"security_alert:{event_type}:{source_ip}", 3600, str(alert_data))
                print(f"   💾 Cached: {event_type} from {source_ip}")
            
            # Analyze security breach impact
            print(f"\n📊 Security Breach Analysis:")
            
            cursor.execute("""
                SELECT event_type, severity, COUNT(*) as count
                FROM security_events
                GROUP BY event_type, severity
                ORDER BY severity, count DESC
            """)
            
            breach_analysis = cursor.fetchall()
            for event_type, severity, count in breach_analysis:
                severity_icon = "🚨" if severity == "CRITICAL" else "⚠️"
                print(f"   {severity_icon} {event_type}: {count} {severity} events")
            
            # Test security response
            print(f"\n🧪 Testing Security Response:")
            
            # Test 1: Block suspicious IPs
            suspicious_ips = ["192.168.1.100", "203.0.113.1", "198.51.100.10"]
            for ip in suspicious_ips:
                r.setex(f"blocked_ip:{ip}", 86400, "blocked")  # Block for 24 hours
                print(f"   🚫 Blocked IP: {ip}")
            
            # Test 2: Enable security mode
            r.setex("security_mode", 3600, "enabled")
            print(f"   🔒 Security mode enabled")
            
            # Test 3: Log security events
            cursor.execute("SELECT COUNT(*) FROM security_events")
            event_count = cursor.fetchone()[0]
            print(f"   📝 Security events logged: {event_count}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Security breach test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement security monitoring and incident response!")

def main():
    """Run Real-World Scenarios Chaos"""
    print("💥 LAB 10: REAL-WORLD SCENARIOS CHAOS - Production Disasters")
    print("=" * 60)
    print("🚨 This is where you build real-world production resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_production_disaster()
        chaos_cascading_failures()
        chaos_data_corruption()
        chaos_security_breach()
        
        print("\n🎉 REAL-WORLD SCENARIOS CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Production disasters happen - implement disaster recovery plans")
        print("• Cascading failures are real - implement circuit breakers and bulkheads")
        print("• Data corruption occurs - implement validation and integrity checks")
        print("• Security breaches happen - implement monitoring and incident response")
        print("• Real-world production chaos is complex - TestContainers helps you prepare!")
        print("\n🎉 Congratulations! You've mastered TestContainers chaos engineering!")
        print("💪 You're now ready for any production disaster!")
        
    except Exception as e:
        print(f"❌ Real-world scenarios chaos failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
