#!/usr/bin/env python3
"""
Lab 10: Real-World Scenarios - Working Examples
===============================================

Learn real-world TestContainers scenarios including production-like
testing, monitoring, and deployment patterns.
"""

import os
import sys
import time
import threading
import json
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

def demo_ecommerce_platform():
    """Complete e-commerce platform simulation"""
    print("\n🛒 E-commerce Platform Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Setup database
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
        
        # Create e-commerce schema
        cursor.execute("""
            CREATE TABLE customers (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                category VARCHAR(50) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                total DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """)
        
        print("📊 E-commerce Schema Created: customers, products, orders, order_items")
        
        # Insert real e-commerce data
        print("📝 Creating E-commerce Data:")
        
        # Products
        products = [
            ("MacBook Pro", 2499.99, 10, "Electronics"),
            ("iPhone", 999.99, 25, "Electronics"),
            ("iPad", 599.99, 15, "Electronics"),
            ("Coffee Mug", 12.99, 100, "Home"),
            ("Python Book", 49.99, 50, "Books")
        ]
        
        for name, price, stock, category in products:
            cursor.execute(
                "INSERT INTO products (name, price, stock, category) VALUES (%s, %s, %s, %s)",
                (name, price, stock, category)
            )
            print(f"   + {name}: ${price} (Stock: {stock}, Category: {category})")
        
        # Customers
        customers = [
            ("alice@example.com", "Alice Johnson"),
            ("bob@example.com", "Bob Smith"),
            ("carol@example.com", "Carol Davis")
        ]
        
        for email, name in customers:
            cursor.execute(
                "INSERT INTO customers (email, name) VALUES (%s, %s)",
                (email, name)
            )
            print(f"   + {name} ({email})")
        
        conn.commit()
        
        # Simulate real e-commerce operations
        print(f"\n🛒 Simulating E-commerce Operations:")
        
        # Customer 1 places order
        print(f"   👤 Alice places order:")
        cursor.execute("SELECT id FROM customers WHERE email = 'alice@example.com'")
        alice_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO orders (customer_id, total) 
            VALUES (%s, %s) RETURNING id
        """, (alice_id, 2499.99))
        order_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, 1, 1, 2499.99))  # MacBook Pro
        
        print(f"      📦 Order {order_id}: MacBook Pro x1 - $2499.99")
        
        # Customer 2 places order
        print(f"   👤 Bob places order:")
        cursor.execute("SELECT id FROM customers WHERE email = 'bob@example.com'")
        bob_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO orders (customer_id, total) 
            VALUES (%s, %s) RETURNING id
        """, (bob_id, 1062.98))
        order_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, 2, 1, 999.99))  # iPhone
        
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, 4, 2, 12.99))  # Coffee Mug x2
        
        print(f"      📦 Order {order_id}: iPhone x1 + Coffee Mug x2 - $1062.98")
        
        conn.commit()
        
        # Cache popular products in Redis
        print(f"\n💾 Caching Popular Products:")
        cursor.execute("""
            SELECT p.name, p.price, p.stock, p.category
            FROM products p
            ORDER BY p.price DESC
            LIMIT 3
        """)
        
        popular_products = cursor.fetchall()
        for name, price, stock, category in popular_products:
            product_data = {
                "name": name,
                "price": float(price),
                "stock": stock,
                "category": category
            }
            r.setex(f"product:{name}", 300, json.dumps(product_data))
            print(f"   💾 Cached: {name} - ${price} (TTL: 300s)")
        
        # Generate real-time analytics
        print(f"\n📊 Real-time Analytics:")
        
        # Order summary
        cursor.execute("""
            SELECT COUNT(*) as total_orders, 
                   SUM(total) as total_revenue,
                   AVG(total) as avg_order_value
            FROM orders
        """)
        
        order_stats = cursor.fetchone()
        print(f"   📦 Orders: {order_stats[0]} total, ${order_stats[1]:.2f} revenue, ${order_stats[2]:.2f} avg")
        
        # Product performance
        cursor.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold,
                   SUM(oi.quantity * oi.price) as total_revenue
            FROM products p
            JOIN order_items oi ON p.id = oi.product_id
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
        """)
        
        product_performance = cursor.fetchall()
        print(f"   📈 Product Performance:")
        for name, sold, revenue in product_performance:
            print(f"      {name}: {sold} sold, ${revenue:.2f} revenue")
        
        # Customer analysis
        cursor.execute("""
            SELECT c.name, c.email, COUNT(o.id) as order_count,
                   COALESCE(SUM(o.total), 0) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.email
            ORDER BY total_spent DESC
        """)
        
        customer_analysis = cursor.fetchall()
        print(f"   👥 Customer Analysis:")
        for name, email, orders, spent in customer_analysis:
            print(f"      {name}: {orders} orders, ${spent:.2f} spent")
        
        cursor.close()
        conn.close()

def demo_monitoring_system():
    """Production monitoring system simulation"""
    print("\n📊 Monitoring System Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Setup monitoring database
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
        
        # Create monitoring schema
        cursor.execute("""
            CREATE TABLE metrics (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(50) NOT NULL,
                metric_name VARCHAR(100) NOT NULL,
                value DECIMAL(10,2) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE alerts (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(50) NOT NULL,
                alert_type VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                severity VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("📊 Monitoring Schema Created: metrics, alerts")
        
        # Simulate real monitoring data
        print("📝 Generating Monitoring Data:")
        
        # Generate metrics for different services
        services = ["user-service", "order-service", "payment-service", "notification-service"]
        metrics = ["cpu_usage", "memory_usage", "response_time", "error_rate", "throughput"]
        
        for service in services:
            for metric in metrics:
                # Generate realistic metric values
                if metric == "cpu_usage":
                    value = 45.5 + (hash(service) % 30)  # 45-75%
                elif metric == "memory_usage":
                    value = 60.2 + (hash(service) % 25)  # 60-85%
                elif metric == "response_time":
                    value = 120.5 + (hash(service) % 200)  # 120-320ms
                elif metric == "error_rate":
                    value = 0.5 + (hash(service) % 5)  # 0.5-5.5%
                else:  # throughput
                    value = 1000 + (hash(service) % 2000)  # 1000-3000 req/s
                
                cursor.execute("""
                    INSERT INTO metrics (service_name, metric_name, value)
                    VALUES (%s, %s, %s)
                """, (service, metric, value))
                
                print(f"   + {service}: {metric} = {value:.2f}")
        
        conn.commit()
        
        # Generate alerts for critical metrics
        print(f"\n🚨 Generating Alerts:")
        
        # Check for critical metrics
        cursor.execute("""
            SELECT service_name, metric_name, value
            FROM metrics
            WHERE (metric_name = 'cpu_usage' AND value > 80) OR
                  (metric_name = 'memory_usage' AND value > 85) OR
                  (metric_name = 'response_time' AND value > 500) OR
                  (metric_name = 'error_rate' AND value > 5)
        """)
        
        critical_metrics = cursor.fetchall()
        for service, metric, value in critical_metrics:
            severity = "HIGH" if value > 90 else "MEDIUM"
            message = f"{metric} is {value:.2f} for {service}"
            
            cursor.execute("""
                INSERT INTO alerts (service_name, alert_type, message, severity)
                VALUES (%s, %s, %s, %s)
            """, (service, metric, message, severity))
            
            print(f"   🚨 {severity}: {message}")
        
        conn.commit()
        
        # Store real-time metrics in Redis
        print(f"\n💾 Storing Real-time Metrics in Redis:")
        
        cursor.execute("""
            SELECT service_name, metric_name, value, timestamp
            FROM metrics
            ORDER BY timestamp DESC
            LIMIT 20
        """)
        
        recent_metrics = cursor.fetchall()
        for service, metric, value, timestamp in recent_metrics:
            metric_data = {
                "service": service,
                "metric": metric,
                "value": float(value),
                "timestamp": timestamp.isoformat()
            }
            r.setex(f"metric:{service}:{metric}", 60, json.dumps(metric_data))
            print(f"   💾 Cached: {service}:{metric} = {value:.2f}")
        
        # Generate monitoring dashboard data
        print(f"\n📊 Monitoring Dashboard:")
        
        # Service health summary
        cursor.execute("""
            SELECT service_name, 
                   AVG(CASE WHEN metric_name = 'cpu_usage' THEN value END) as avg_cpu,
                   AVG(CASE WHEN metric_name = 'memory_usage' THEN value END) as avg_memory,
                   AVG(CASE WHEN metric_name = 'response_time' THEN value END) as avg_response_time
            FROM metrics
            GROUP BY service_name
            ORDER BY service_name
        """)
        
        service_health = cursor.fetchall()
        print(f"   🏥 Service Health Summary:")
        for service, cpu, memory, response_time in service_health:
            health_status = "✅ Healthy" if cpu < 70 and memory < 80 and response_time < 300 else "⚠️ Warning"
            print(f"      {service}: {health_status}")
            print(f"         CPU: {cpu:.1f}%, Memory: {memory:.1f}%, Response: {response_time:.1f}ms")
        
        # Alert summary
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM alerts
            GROUP BY severity
            ORDER BY severity
        """)
        
        alert_summary = cursor.fetchall()
        print(f"   🚨 Alert Summary:")
        for severity, count in alert_summary:
            print(f"      {severity}: {count} alerts")
        
        cursor.close()
        conn.close()

def demo_deployment_pipeline():
    """Deployment pipeline simulation"""
    print("\n🚀 Deployment Pipeline Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Setup deployment tracking
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
        
        # Create deployment schema
        cursor.execute("""
            CREATE TABLE deployments (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(50) NOT NULL,
                version VARCHAR(20) NOT NULL,
                environment VARCHAR(20) NOT NULL,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE deployment_tests (
                id SERIAL PRIMARY KEY,
                deployment_id INTEGER REFERENCES deployments(id),
                test_name VARCHAR(100) NOT NULL,
                status VARCHAR(20) NOT NULL,
                duration INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("📊 Deployment Schema Created: deployments, deployment_tests")
        
        # Simulate deployment pipeline
        print("🚀 Simulating Deployment Pipeline:")
        
        # Deploy services
        services = [
            ("user-service", "v1.2.3", "staging"),
            ("order-service", "v2.1.0", "staging"),
            ("payment-service", "v1.5.2", "staging"),
            ("notification-service", "v1.0.1", "staging")
        ]
        
        for service, version, environment in services:
            cursor.execute("""
                INSERT INTO deployments (service_name, version, environment, status)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (service, version, environment, "deploying"))
            
            deployment_id = cursor.fetchone()[0]
            print(f"   🚀 Deploying {service} {version} to {environment}")
            
            # Run deployment tests
            tests = [
                ("unit_tests", "passed", 45),
                ("integration_tests", "passed", 120),
                ("performance_tests", "passed", 300),
                ("security_tests", "passed", 90)
            ]
            
            for test_name, status, duration in tests:
                cursor.execute("""
                    INSERT INTO deployment_tests (deployment_id, test_name, status, duration)
                    VALUES (%s, %s, %s, %s)
                """, (deployment_id, test_name, status, duration))
                
                print(f"      ✅ {test_name}: {status} ({duration}s)")
            
            # Update deployment status
            cursor.execute("""
                UPDATE deployments SET status = 'deployed' WHERE id = %s
            """, (deployment_id,))
            
            print(f"   ✅ {service} {version} deployed successfully")
        
        conn.commit()
        
        # Store deployment status in Redis
        print(f"\n💾 Storing Deployment Status in Redis:")
        
        cursor.execute("""
            SELECT service_name, version, environment, status, created_at
            FROM deployments
            ORDER BY created_at DESC
        """)
        
        deployments = cursor.fetchall()
        for service, version, env, status, created_at in deployments:
            deployment_data = {
                "service": service,
                "version": version,
                "environment": env,
                "status": status,
                "deployed_at": created_at.isoformat()
            }
            r.setex(f"deployment:{service}", 3600, json.dumps(deployment_data))
            print(f"   💾 Cached: {service} {version} ({status})")
        
        # Generate deployment report
        print(f"\n📊 Deployment Report:")
        
        # Deployment summary
        cursor.execute("""
            SELECT environment, COUNT(*) as total_deployments,
                   SUM(CASE WHEN status = 'deployed' THEN 1 ELSE 0 END) as successful_deployments
            FROM deployments
            GROUP BY environment
        """)
        
        deployment_summary = cursor.fetchall()
        print(f"   📈 Deployment Summary:")
        for env, total, successful in deployment_summary:
            success_rate = (successful / total) * 100 if total > 0 else 0
            print(f"      {env}: {successful}/{total} deployments ({success_rate:.1f}% success rate)")
        
        # Test performance
        cursor.execute("""
            SELECT test_name, 
                   AVG(duration) as avg_duration,
                   COUNT(*) as total_runs,
                   SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_runs
            FROM deployment_tests
            GROUP BY test_name
            ORDER BY avg_duration DESC
        """)
        
        test_performance = cursor.fetchall()
        print(f"   🧪 Test Performance:")
        for test_name, avg_duration, total_runs, passed_runs in test_performance:
            pass_rate = (passed_runs / total_runs) * 100 if total_runs > 0 else 0
            print(f"      {test_name}: {avg_duration:.1f}s avg, {passed_runs}/{total_runs} passed ({pass_rate:.1f}%)")
        
        cursor.close()
        conn.close()

def main():
    """Run Lab 10 - Real-World Scenarios"""
    print("🚀 LAB 10: Real-World Scenarios - Working Examples")
    print("=" * 60)
    print("✨ Master real-world TestContainers scenarios!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_ecommerce_platform()
        demo_monitoring_system()
        demo_deployment_pipeline()
        
        print("\n✅ Lab 10 completed successfully!")
        print("Key concepts learned:")
        print("• Complete e-commerce platform simulation")
        print("• Production monitoring and alerting systems")
        print("• Deployment pipeline and testing automation")
        print("• Real-world data patterns and analytics")
        print("• Production-ready TestContainers scenarios")
        print("\n🎉 Congratulations! You've mastered TestContainers!")
        print("💪 You're now ready for production testing challenges!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()