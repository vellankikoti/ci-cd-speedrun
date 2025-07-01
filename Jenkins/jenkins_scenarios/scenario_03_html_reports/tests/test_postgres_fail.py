"""
Scenario 03: HTML Reports Chaos - Postgres Database Tests (FAIL)

These tests simulate real-world database failures that should
always fail to demonstrate common enterprise database problems.
"""

import pytest
import psycopg2
import time
from testcontainers.postgres import PostgresContainer
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, IntegrityError


class TestPostgresFail:
    """Test PostgreSQL database scenarios that should fail"""

    def test_postgres_connection_with_wrong_credentials(self):
        """Test database connection with incorrect credentials"""
        with PostgresContainer("postgres:14") as postgres:
            # Get the correct connection details
            host = postgres.get_container_host_ip()
            port = postgres.get_exposed_port(5432)
            
            # Try to connect with wrong credentials
            wrong_connection_url = f"postgresql://wrong_user:wrong_password@{host}:{port}/test"
            
            try:
                engine = create_engine(wrong_connection_url)
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    # If we reach here, the test should fail
                    assert False, "Connection should fail with wrong credentials"
            except OperationalError:
                # Expected error, but we want the test to fail anyway
                assert False, "Authentication failed as expected, but test designed to fail"

    def test_postgres_connection_to_nonexistent_database(self):
        """Test connection to a database that doesn't exist"""
        with PostgresContainer("postgres:14") as postgres:
            host = postgres.get_container_host_ip()
            port = postgres.get_exposed_port(5432)
            
            # Try to connect to non-existent database
            wrong_db_url = f"postgresql://test:test@{host}:{port}/nonexistent_database"
            
            try:
                engine = create_engine(wrong_db_url)
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    # This should fail
                    assert False, "Should not be able to connect to non-existent database"
            except OperationalError:
                # Expected, but test should still fail
                assert False, "Database not found as expected, but test designed to fail"

    def test_postgres_table_constraint_violations(self):
        """Test database constraint violations"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create table with strict constraints
                conn.execute(text("""
                    CREATE TABLE test_constraints (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        age INTEGER CHECK (age >= 18 AND age <= 120),
                        status VARCHAR(20) CHECK (status IN ('active', 'inactive'))
                    )
                """))
                conn.commit()
                
                # Insert valid data first
                conn.execute(text("""
                    INSERT INTO test_constraints (email, age, status) 
                    VALUES ('test@example.com', 25, 'active')
                """))
                conn.commit()
                
                # Try to insert duplicate email (unique constraint violation)
                try:
                    conn.execute(text("""
                        INSERT INTO test_constraints (email, age, status) 
                        VALUES ('test@example.com', 30, 'active')
                    """))
                    conn.commit()
                    assert False, "Should not allow duplicate email addresses"
                except IntegrityError:
                    conn.rollback()
                    assert False, "Constraint violation as expected, but test designed to fail"

    def test_postgres_connection_timeout(self):
        """Test database connection timeout"""
        # This test simulates a connection timeout scenario
        try:
            # Try to connect to a non-responsive database
            engine = create_engine(
                "postgresql://user:pass@192.0.2.1:5432/test",  # Non-routable IP
                connect_args={"connect_timeout": 1}  # Very short timeout
            )
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                # Should not reach here
                assert False, "Connection should timeout"
                
        except OperationalError:
            # Expected timeout, but test should fail
            assert False, "Connection timed out as expected, but test designed to fail"

    def test_postgres_deadlock_simulation(self):
        """Test database deadlock scenario"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            
            # Create two separate engines for simulating concurrent transactions
            engine1 = create_engine(connection_url)
            engine2 = create_engine(connection_url)
            
            with engine1.connect() as conn1, engine2.connect() as conn2:
                # Setup test table
                conn1.execute(text("""
                    CREATE TABLE test_deadlock (
                        id INTEGER PRIMARY KEY,
                        value INTEGER
                    )
                """))
                conn1.execute(text("""
                    INSERT INTO test_deadlock (id, value) VALUES (1, 100), (2, 200)
                """))
                conn1.commit()
                
                try:
                    # Start transactions that will create deadlock
                    trans1 = conn1.begin()
                    trans2 = conn2.begin()
                    
                    # Transaction 1: Update row 1, then try to update row 2
                    conn1.execute(text("UPDATE test_deadlock SET value = 101 WHERE id = 1"))
                    
                    # Transaction 2: Update row 2, then try to update row 1
                    conn2.execute(text("UPDATE test_deadlock SET value = 201 WHERE id = 2"))
                    
                    # Now both try to update the other's locked row (potential deadlock)
                    conn1.execute(text("UPDATE test_deadlock SET value = 102 WHERE id = 2"))
                    conn2.execute(text("UPDATE test_deadlock SET value = 103 WHERE id = 1"))
                    
                    trans1.commit()
                    trans2.commit()
                    
                    # If we reach here without deadlock, test should fail
                    assert False, "Expected deadlock did not occur"
                    
                except Exception:
                    # Deadlock or other error occurred
                    try:
                        trans1.rollback()
                    except:
                        pass
                    try:
                        trans2.rollback()
                    except:
                        pass
                    
                    # Even though deadlock occurred as expected, test should fail
                    assert False, "Deadlock occurred as expected, but test designed to fail"

    def test_postgres_invalid_sql_syntax(self):
        """Test execution of invalid SQL syntax"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                try:
                    # Execute invalid SQL
                    conn.execute(text("SELECT * FROM table_that_does_not_exist"))
                    assert False, "Should not execute invalid SQL successfully"
                except Exception:
                    # Expected error, but test should fail
                    assert False, "SQL error as expected, but test designed to fail"

    def test_postgres_data_type_mismatch(self):
        """Test data type mismatches and invalid operations"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create table with specific data types
                conn.execute(text("""
                    CREATE TABLE test_types (
                        id SERIAL PRIMARY KEY,
                        number_field INTEGER,
                        date_field DATE
                    )
                """))
                conn.commit()
                
                try:
                    # Try to insert incompatible data types
                    conn.execute(text("""
                        INSERT INTO test_types (number_field, date_field) 
                        VALUES ('not_a_number', 'not_a_date')
                    """))
                    conn.commit()
                    assert False, "Should not accept invalid data types"
                except Exception:
                    conn.rollback()
                    assert False, "Data type error as expected, but test designed to fail"

    def test_postgres_transaction_isolation_failure(self):
        """Test transaction isolation level failures"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine1 = create_engine(connection_url)
            engine2 = create_engine(connection_url)
            
            with engine1.connect() as conn1, engine2.connect() as conn2:
                # Setup test data
                conn1.execute(text("""
                    CREATE TABLE test_isolation (
                        id INTEGER PRIMARY KEY,
                        balance DECIMAL(10,2)
                    )
                """))
                conn1.execute(text("""
                    INSERT INTO test_isolation (id, balance) VALUES (1, 1000.00)
                """))
                conn1.commit()
                
                # Set strict isolation level
                conn1.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                conn2.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                
                try:
                    trans1 = conn1.begin()
                    trans2 = conn2.begin()
                    
                    # Both transactions read the same data
                    result1 = conn1.execute(text("SELECT balance FROM test_isolation WHERE id = 1"))
                    balance1 = result1.fetchone()[0]
                    
                    result2 = conn2.execute(text("SELECT balance FROM test_isolation WHERE id = 1"))
                    balance2 = result2.fetchone()[0]
                    
                    # Both try to update based on what they read
                    conn1.execute(text("UPDATE test_isolation SET balance = :balance WHERE id = 1"), 
                                 {'balance': balance1 - 100})
                    conn2.execute(text("UPDATE test_isolation SET balance = :balance WHERE id = 1"), 
                                 {'balance': balance2 - 50})
                    
                    trans1.commit()
                    trans2.commit()
                    
                    # If both commits succeed, we have isolation violation
                    assert False, "Both transactions should not succeed with SERIALIZABLE isolation"
                    
                except Exception:
                    # Serialization failure expected
                    try:
                        trans1.rollback()
                    except:
                        pass
                    try:
                        trans2.rollback()
                    except:
                        pass
                    
                    assert False, "Serialization failure as expected, but test designed to fail"

    def test_postgres_resource_exhaustion(self):
        """Test database resource exhaustion scenarios"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url, pool_size=1, max_overflow=0)
            
            connections = []
            try:
                # Try to exhaust connection pool
                for i in range(5):  # Try to open more connections than available
                    conn = engine.connect()
                    connections.append(conn)
                    
                # If we get here, test should fail
                assert False, "Should not be able to open unlimited connections"
                
            except Exception:
                # Expected resource exhaustion
                assert False, "Connection pool exhausted as expected, but test designed to fail"
            finally:
                # Clean up connections
                for conn in connections:
                    try:
                        conn.close()
                    except:
                        pass

    def test_postgres_index_corruption_simulation(self):
        """Test behavior with corrupted indexes"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create table and index
                conn.execute(text("""
                    CREATE TABLE test_index_corruption (
                        id SERIAL PRIMARY KEY,
                        searchable_field VARCHAR(100)
                    )
                """))
                
                conn.execute(text("""
                    CREATE INDEX idx_searchable ON test_index_corruption(searchable_field)
                """))
                
                # Insert data
                for i in range(100):
                    conn.execute(text("""
                        INSERT INTO test_index_corruption (searchable_field) 
                        VALUES (:field)
                    """), {'field': f'value_{i}'})
                conn.commit()
                
                # Simulate index corruption by dropping and recreating with wrong definition
                try:
                    conn.execute(text("DROP INDEX idx_searchable"))
                    
                    # Create a "corrupted" index with different definition
                    conn.execute(text("""
                        CREATE INDEX idx_searchable ON test_index_corruption(id)  -- Wrong column
                    """))
                    conn.commit()
                    
                    # Query should work but performance will be degraded
                    result = conn.execute(text("""
                        SELECT COUNT(*) FROM test_index_corruption 
                        WHERE searchable_field = 'value_50'
                    """))
                    count = result.fetchone()[0]
                    
                    # This assertion will pass, but we want the test to fail anyway
                    assert count == 1, "Query should find the record, but index is corrupted"
                    assert False, "Index corruption not properly detected"
                    
                except Exception:
                    assert False, "Index corruption simulation failed, but test designed to fail"

    def test_postgres_backup_corruption(self):
        """Test corrupted backup scenarios"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create test data
                conn.execute(text("""
                    CREATE TABLE test_backup_corruption (
                        id SERIAL PRIMARY KEY,
                        critical_data TEXT NOT NULL
                    )
                """))
                
                original_data = ['Important record 1', 'Critical data 2', 'Essential info 3']
                for data in original_data:
                    conn.execute(text("""
                        INSERT INTO test_backup_corruption (critical_data) VALUES (:data)
                    """), {'data': data})
                conn.commit()
                
                # Simulate backup corruption by modifying data
                conn.execute(text("""
                    UPDATE test_backup_corruption 
                    SET critical_data = 'CORRUPTED_DATA' 
                    WHERE id = 2
                """))
                conn.commit()
                
                # Verify corruption
                result = conn.execute(text("""
                    SELECT critical_data FROM test_backup_corruption WHERE id = 2
                """))
                corrupted_data = result.fetchone()[0]
                
                # This should fail because data is corrupted
                assert corrupted_data == 'Critical data 2', "Data should not be corrupted"
                assert False, "Backup corruption not detected properly"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])