"""
Scenario 03: HTML Reports Chaos - Postgres Database Tests (PASS)

These tests demonstrate proper database testing patterns using testcontainers
that should always pass with a healthy PostgreSQL database.
"""

import pytest
import psycopg2
import time
from testcontainers.postgres import PostgresContainer
import sqlalchemy
from sqlalchemy import create_engine, text


class TestPostgresPass:
    """Test PostgreSQL database scenarios that should pass"""

    def test_postgres_container_startup(self):
        """Test that PostgreSQL container starts successfully"""
        with PostgresContainer("postgres:14") as postgres:
            # Container should start successfully
            assert postgres.get_container_host_ip() is not None, "Container should have host IP"
            assert postgres.get_exposed_port(5432) is not None, "Container should expose PostgreSQL port"
            
            # Get connection details
            connection_url = postgres.get_connection_url()
            assert connection_url.startswith("postgresql://"), "Connection URL should be PostgreSQL format"
            
            # Test basic connection
            engine = create_engine(connection_url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test_value"))
                row = result.fetchone()
                assert row[0] == 1, "Basic query should return expected value"

    def test_postgres_database_operations(self):
        """Test basic database operations work correctly"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create test table
                conn.execute(text("""
                    CREATE TABLE test_users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                
                # Insert test data
                conn.execute(text("""
                    INSERT INTO test_users (username, email) 
                    VALUES ('testuser1', 'test1@example.com'),
                           ('testuser2', 'test2@example.com')
                """))
                conn.commit()
                
                # Query data
                result = conn.execute(text("SELECT COUNT(*) FROM test_users"))
                count = result.fetchone()[0]
                assert count == 2, "Should have inserted 2 users"
                
                # Update data
                conn.execute(text("""
                    UPDATE test_users 
                    SET email = 'updated@example.com' 
                    WHERE username = 'testuser1'
                """))
                conn.commit()
                
                # Verify update
                result = conn.execute(text("""
                    SELECT email FROM test_users 
                    WHERE username = 'testuser1'
                """))
                email = result.fetchone()[0]
                assert email == 'updated@example.com', "Email should be updated"
                
                # Delete data
                conn.execute(text("DELETE FROM test_users WHERE username = 'testuser2'"))
                conn.commit()
                
                # Verify deletion
                result = conn.execute(text("SELECT COUNT(*) FROM test_users"))
                count = result.fetchone()[0]
                assert count == 1, "Should have 1 user after deletion"

    def test_postgres_transactions_and_rollback(self):
        """Test database transactions and rollback functionality"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create test table
                conn.execute(text("""
                    CREATE TABLE test_accounts (
                        id SERIAL PRIMARY KEY,
                        account_name VARCHAR(50) NOT NULL,
                        balance DECIMAL(10,2) DEFAULT 0.00
                    )
                """))
                conn.commit()
                
                # Insert initial data
                conn.execute(text("""
                    INSERT INTO test_accounts (account_name, balance) 
                    VALUES ('Account A', 1000.00), ('Account B', 500.00)
                """))
                conn.commit()
                
                # Test successful transaction
                trans = conn.begin()
                try:
                    # Transfer money from Account A to Account B
                    conn.execute(text("""
                        UPDATE test_accounts 
                        SET balance = balance - 100.00 
                        WHERE account_name = 'Account A'
                    """))
                    
                    conn.execute(text("""
                        UPDATE test_accounts 
                        SET balance = balance + 100.00 
                        WHERE account_name = 'Account B'
                    """))
                    
                    trans.commit()
                    
                    # Verify balances after successful transaction
                    result = conn.execute(text("""
                        SELECT account_name, balance FROM test_accounts 
                        ORDER BY account_name
                    """))
                    accounts = result.fetchall()
                    
                    assert accounts[0][1] == 900.00, "Account A should have 900.00"
                    assert accounts[1][1] == 600.00, "Account B should have 600.00"
                    
                except Exception:
                    trans.rollback()
                    raise
                
                # Test transaction rollback
                initial_balance_a = conn.execute(text("""
                    SELECT balance FROM test_accounts WHERE account_name = 'Account A'
                """)).fetchone()[0]
                
                trans = conn.begin()
                try:
                    # Attempt invalid operation (insufficient funds)
                    conn.execute(text("""
                        UPDATE test_accounts 
                        SET balance = balance - 2000.00 
                        WHERE account_name = 'Account A'
                    """))
                    
                    # Check if balance would go negative
                    result = conn.execute(text("""
                        SELECT balance FROM test_accounts WHERE account_name = 'Account A'
                    """))
                    new_balance = result.fetchone()[0]
                    
                    if new_balance < 0:
                        raise ValueError("Insufficient funds")
                    
                    trans.commit()
                    
                except ValueError:
                    trans.rollback()
                    
                    # Verify rollback worked
                    result = conn.execute(text("""
                        SELECT balance FROM test_accounts WHERE account_name = 'Account A'
                    """))
                    current_balance = result.fetchone()[0]
                    assert current_balance == initial_balance_a, "Balance should be restored after rollback"

    def test_postgres_indexes_and_performance(self):
        """Test database indexes and query performance"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create test table with index
                conn.execute(text("""
                    CREATE TABLE test_products (
                        id SERIAL PRIMARY KEY,
                        product_name VARCHAR(100) NOT NULL,
                        category VARCHAR(50) NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create index on category for faster queries
                conn.execute(text("""
                    CREATE INDEX idx_products_category ON test_products(category)
                """))
                conn.commit()
                
                # Insert test data
                categories = ['Electronics', 'Books', 'Clothing', 'Home']
                for i in range(1000):
                    category = categories[i % len(categories)]
                    conn.execute(text("""
                        INSERT INTO test_products (product_name, category, price) 
                        VALUES (:name, :category, :price)
                    """), {
                        'name': f'Product {i+1}',
                        'category': category,
                        'price': (i % 100) + 10.99
                    })
                conn.commit()
                
                # Test query performance with index
                start_time = time.time()
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM test_products WHERE category = 'Electronics'
                """))
                query_time = time.time() - start_time
                
                count = result.fetchone()[0]
                assert count == 250, "Should have 250 Electronics products"
                assert query_time < 1.0, "Indexed query should be fast (< 1 second)"
                
                # Verify index usage with EXPLAIN
                result = conn.execute(text("""
                    EXPLAIN (FORMAT JSON) 
                    SELECT * FROM test_products WHERE category = 'Books'
                """))
                explain_result = result.fetchone()[0]
                
                # The query plan should use the index
                assert 'Index Scan' in str(explain_result) or 'Bitmap' in str(explain_result), \
                    "Query should use index for better performance"

    def test_postgres_data_types_and_constraints(self):
        """Test various PostgreSQL data types and constraints"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create table with various data types and constraints
                conn.execute(text("""
                    CREATE TABLE test_datatypes (
                        id SERIAL PRIMARY KEY,
                        text_field TEXT NOT NULL,
                        varchar_field VARCHAR(50),
                        integer_field INTEGER CHECK (integer_field > 0),
                        decimal_field DECIMAL(10,2),
                        boolean_field BOOLEAN DEFAULT FALSE,
                        date_field DATE,
                        timestamp_field TIMESTAMP,
                        json_field JSONB,
                        array_field INTEGER[],
                        unique_field VARCHAR(100) UNIQUE
                    )
                """))
                conn.commit()
                
                # Insert test data with various types
                conn.execute(text("""
                    INSERT INTO test_datatypes (
                        text_field, varchar_field, integer_field, decimal_field,
                        boolean_field, date_field, timestamp_field, json_field,
                        array_field, unique_field
                    ) VALUES (
                        'This is a long text field',
                        'Short text',
                        42,
                        123.45,
                        TRUE,
                        '2024-01-01',
                        '2024-01-01 12:00:00',
                        '{"name": "test", "value": 123}',
                        '{1, 2, 3, 4, 5}',
                        'unique_value_1'
                    )
                """))
                conn.commit()
                
                # Query and validate data types
                result = conn.execute(text("SELECT * FROM test_datatypes WHERE id = 1"))
                row = result.fetchone()
                
                assert row[1] == 'This is a long text field', "Text field should match"
                assert row[2] == 'Short text', "Varchar field should match"
                assert row[3] == 42, "Integer field should match"
                assert row[4] == 123.45, "Decimal field should match"
                assert row[5] is True, "Boolean field should be True"
                
                # Test JSON operations
                result = conn.execute(text("""
                    SELECT json_field->>'name' as name, 
                           (json_field->>'value')::INTEGER as value
                    FROM test_datatypes WHERE id = 1
                """))
                json_row = result.fetchone()
                assert json_row[0] == 'test', "JSON name field should match"
                assert json_row[1] == 123, "JSON value field should match"
                
                # Test array operations
                result = conn.execute(text("""
                    SELECT array_length(array_field, 1) as array_len,
                           array_field[1] as first_element
                    FROM test_datatypes WHERE id = 1
                """))
                array_row = result.fetchone()
                assert array_row[0] == 5, "Array should have 5 elements"
                assert array_row[1] == 1, "First array element should be 1"

    def test_postgres_connection_pooling(self):
        """Test database connection pooling functionality"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            
            # Create engine with connection pooling
            engine = create_engine(
                connection_url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600
            )
            
            # Test multiple concurrent connections
            connections = []
            try:
                # Open multiple connections
                for i in range(3):
                    conn = engine.connect()
                    connections.append(conn)
                    
                    # Execute query on each connection
                    result = conn.execute(text(f"SELECT {i+1} as connection_id"))
                    connection_id = result.fetchone()[0]
                    assert connection_id == i+1, f"Connection {i+1} should work correctly"
                
                # Verify pool statistics
                pool = engine.pool
                assert pool.size() >= 3, "Pool should have at least 3 connections"
                assert pool.checkedout() == 3, "Should have 3 checked out connections"
                
            finally:
                # Clean up connections
                for conn in connections:
                    conn.close()
                
                # Verify connections are returned to pool
                time.sleep(0.1)  # Allow time for cleanup
                assert engine.pool.checkedout() == 0, "All connections should be returned to pool"

    def test_postgres_backup_and_restore_simulation(self):
        """Test database backup and restore simulation"""
        with PostgresContainer("postgres:14") as postgres:
            connection_url = postgres.get_connection_url()
            engine = create_engine(connection_url)
            
            with engine.connect() as conn:
                # Create and populate test table
                conn.execute(text("""
                    CREATE TABLE test_backup (
                        id SERIAL PRIMARY KEY,
                        data VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                original_data = [
                    ('Important data 1',),
                    ('Critical information 2',),
                    ('Essential record 3',)
                ]
                
                for data_tuple in original_data:
                    conn.execute(text("""
                        INSERT INTO test_backup (data) VALUES (:data)
                    """), {'data': data_tuple[0]})
                conn.commit()
                
                # Simulate backup by reading all data
                backup_result = conn.execute(text("""
                    SELECT id, data FROM test_backup ORDER BY id
                """))
                backup_data = backup_result.fetchall()
                
                assert len(backup_data) == 3, "Backup should contain 3 records"
                
                # Simulate data corruption/loss
                conn.execute(text("DELETE FROM test_backup"))
                conn.commit()
                
                # Verify data is gone
                result = conn.execute(text("SELECT COUNT(*) FROM test_backup"))
                count = result.fetchone()[0]
                assert count == 0, "Table should be empty after deletion"
                
                # Simulate restore from backup
                for backup_row in backup_data:
                    conn.execute(text("""
                        INSERT INTO test_backup (id, data) VALUES (:id, :data)
                    """), {'id': backup_row[0], 'data': backup_row[1]})
                conn.commit()
                
                # Reset sequence to continue from correct value
                conn.execute(text("""
                    SELECT setval('test_backup_id_seq', (SELECT MAX(id) FROM test_backup))
                """))
                conn.commit()
                
                # Verify restore was successful
                restored_result = conn.execute(text("""
                    SELECT COUNT(*) FROM test_backup
                """))
                restored_count = restored_result.fetchone()[0]
                assert restored_count == 3, "All data should be restored"
                
                # Verify data integrity
                result = conn.execute(text("""
                    SELECT data FROM test_backup ORDER BY id
                """))
                restored_data = [row[0] for row in result.fetchall()]
                expected_data = [data_tuple[0] for data_tuple in original_data]
                assert restored_data == expected_data, "Restored data should match original data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])