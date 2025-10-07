#!/usr/bin/env python3
"""
Test Master - Database Module
Simple database abstraction for testing with TestContainers.
"""

import os
import sqlite3
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class User:
    """User model for database operations."""
    id: int
    name: str
    email: str

class DatabaseManager:
    """Simple database manager for testing purposes."""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager."""
        self.db_path = db_path or os.environ.get('DATABASE_URL', 'test_master.db')
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1')
                return True
        except Exception:
            return False
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (name, email) VALUES (?, ?)',
                    (name, email)
                )
                user_id = cursor.lastrowid
                conn.commit()
                return User(id=user_id, name=name, email=email)
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")
        except Exception as e:
            raise Exception(f"Error creating user: {e}")
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                if row:
                    return User(id=row[0], name=row[1], email=row[2])
                return None
        except Exception as e:
            raise Exception(f"Error getting user: {e}")
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, email FROM users ORDER BY created_at DESC')
                rows = cursor.fetchall()
                return [User(id=row[0], name=row[1], email=row[2]) for row in rows]
        except Exception as e:
            raise Exception(f"Error getting users: {e}")
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> Optional[User]:
        """Update user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build update query dynamically
                updates = []
                params = []
                
                if name is not None:
                    updates.append('name = ?')
                    params.append(name)
                
                if email is not None:
                    updates.append('email = ?')
                    params.append(email)
                
                if not updates:
                    return self.get_user(user_id)
                
                params.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return self.get_user(user_id)
                return None
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")
        except Exception as e:
            raise Exception(f"Error updating user: {e}")
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error deleting user: {e}")
    
    def clear_all_users(self):
        """Clear all users (for testing)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users')
                conn.commit()
        except Exception as e:
            raise Exception(f"Error clearing users: {e}")
