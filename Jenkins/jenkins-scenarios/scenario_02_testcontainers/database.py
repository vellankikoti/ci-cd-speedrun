#!/usr/bin/env python3
"""
PostgreSQL Database Manager with TestContainers Integration
Real database integration using TestContainers for testing
"""

import os
import logging
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgreSQLDatabaseManager:
    """PostgreSQL database manager with TestContainers support"""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            connection_string: PostgreSQL connection string
                              If None, will use environment variables
        """
        self.connection_string = connection_string or self._build_connection_string()
        self.engine = None
        self.Session = None
        self._initialize_engine()

    def _build_connection_string(self) -> str:
        """Build PostgreSQL connection string from environment variables"""
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'testcontainers_demo')
        username = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'postgres')
        
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    def _initialize_engine(self):
        """Initialize SQLAlchemy engine and session factory"""
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
            )
            self.Session = sessionmaker(bind=self.engine)
            logger.info("✅ Database engine initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize database engine: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Get raw psycopg2 connection with context manager"""
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_session(self):
        """Get SQLAlchemy session with context manager"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def init_database(self):
        """Initialize database with required tables and sample data"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Create users table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)

                    # Create indexes for better performance
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                        CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
                    """)

                    # Check if we have sample data
                    cursor.execute("SELECT COUNT(*) FROM users")
                    user_count = cursor.fetchone()[0]

                    if user_count == 0:
                        # Insert sample data
                        sample_users = [
                            ('John Doe', 'john@example.com'),
                            ('Jane Smith', 'jane@example.com'),
                            ('Bob Johnson', 'bob@example.com'),
                            ('Alice Brown', 'alice@example.com'),
                            ('Charlie Wilson', 'charlie@example.com')
                        ]
                        
                        for name, email in sample_users:
                            cursor.execute(
                                "INSERT INTO users (name, email) VALUES (%s, %s)",
                                (name, email)
                            )

                    conn.commit()
                    logger.info("✅ Database initialized successfully with sample data")
                    
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    def health_check(self) -> bool:
        """Check database health"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users from database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT id, name, email, created_at, updated_at 
                        FROM users 
                        ORDER BY created_at DESC
                    """)
                    users = [dict(row) for row in cursor.fetchall()]
                    logger.info(f"Retrieved {len(users)} users from database")
                    return users
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return []

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT id, name, email, created_at, updated_at 
                        FROM users 
                        WHERE id = %s
                    """, (user_id,))
                    row = cursor.fetchone()
                    return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            return None

    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        INSERT INTO users (name, email) 
                        VALUES (%s, %s) 
                        RETURNING id, name, email, created_at, updated_at
                    """, (name, email))
                    
                    user = dict(cursor.fetchone())
                    conn.commit()
                    logger.info(f"Created user: {user['name']} ({user['email']})")
                    return user
                    
        except psycopg2.IntegrityError as e:
            if 'duplicate key value' in str(e):
                return {'error': 'Email already exists'}
            else:
                return {'error': f'Database constraint violation: {str(e)}'}
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return {'error': str(e)}

    def update_user(self, user_id: int, name: str = None, email: str = None) -> Dict[str, Any]:
        """Update user information"""
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            
            if not updates:
                return {'error': 'No fields to update'}
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(user_id)
            
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(f"""
                        UPDATE users 
                        SET {', '.join(updates)}
                        WHERE id = %s
                        RETURNING id, name, email, created_at, updated_at
                    """, params)
                    
                    user = cursor.fetchone()
                    if user:
                        conn.commit()
                        logger.info(f"Updated user {user_id}")
                        return dict(user)
                    else:
                        return {'error': 'User not found'}
                        
        except psycopg2.IntegrityError as e:
            if 'duplicate key value' in str(e):
                return {'error': 'Email already exists'}
            else:
                return {'error': f'Database constraint violation: {str(e)}'}
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return {'error': str(e)}

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete user by ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # First get the user to return info
                    cursor.execute("""
                        SELECT id, name, email, created_at, updated_at 
                        FROM users 
                        WHERE id = %s
                    """, (user_id,))
                    user = cursor.fetchone()
                    
                    if not user:
                        return {'error': 'User not found'}
                    
                    # Delete the user
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    conn.commit()
                    
                    logger.info(f"Deleted user {user_id}: {user['name']}")
                    return {'message': 'User deleted successfully', 'deleted_user': dict(user)}
                    
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return {'error': str(e)}

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Get user count
                    cursor.execute("SELECT COUNT(*) as user_count FROM users")
                    user_count = cursor.fetchone()['user_count']
                    
                    # Get database size
                    cursor.execute("""
                        SELECT pg_size_pretty(pg_database_size(current_database())) as db_size
                    """)
                    db_size = cursor.fetchone()['db_size']
                    
                    # Get table info
                    cursor.execute("""
                        SELECT 
                            schemaname,
                            tablename,
                            attname as column_name,
                            typname as data_type
                        FROM pg_tables t
                        JOIN pg_attribute a ON a.attrelid = t.tablename::regclass
                        JOIN pg_type ty ON a.atttypid = ty.oid
                        WHERE schemaname = 'public'
                        ORDER BY tablename, a.attnum
                    """)
                    tables = [dict(row) for row in cursor.fetchall()]
                    
                    return {
                        'user_count': user_count,
                        'database_size': db_size,
                        'tables': tables,
                        'connection_string': self.connection_string.split('@')[0] + '@***'  # Hide password
                    }
                    
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)}

    def execute_raw_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute raw SQL query (for advanced use cases)"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params or ())
                    results = [dict(row) for row in cursor.fetchall()]
                    logger.info(f"Executed query, returned {len(results)} rows")
                    return results
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return []

    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


# TestContainers integration class
class TestContainersDatabaseManager(PostgreSQLDatabaseManager):
    """Database manager specifically for TestContainers testing"""
    
    def __init__(self, container_host: str, container_port: int, 
                 database: str = 'test', username: str = 'test', password: str = 'test'):
        """
        Initialize with TestContainers PostgreSQL container
        
        Args:
            container_host: TestContainers container host
            container_port: TestContainers container port
            database: Database name
            username: Database username
            password: Database password
        """
        # Override environment variables for TestContainers
        os.environ['DB_HOST'] = container_host
        os.environ['DB_PORT'] = str(container_port)
        os.environ['DB_NAME'] = database
        os.environ['DB_USER'] = username
        os.environ['DB_PASSWORD'] = password
        
        # Initialize parent class
        super().__init__()
        logger.info(f"✅ TestContainers database manager initialized: {container_host}:{container_port}")


if __name__ == '__main__':
    # Test the database manager
    db = PostgreSQLDatabaseManager()
    
    try:
        # Initialize database
        db.init_database()
        
        # Test health check
        print(f"Database health: {db.health_check()}")
        
        # Test getting users
        users = db.get_users()
        print(f"Found {len(users)} users")
        
        # Test creating a user
        new_user = db.create_user('Test User', 'test@example.com')
        print(f"Created user: {new_user}")
        
        # Test database stats
        stats = db.get_database_stats()
        print(f"Database stats: {stats}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
