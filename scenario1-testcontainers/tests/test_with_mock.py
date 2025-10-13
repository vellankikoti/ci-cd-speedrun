#!/usr/bin/env python3
"""
Test with Mock Database - The Problem
=====================================

This demonstrates why mocks can be dangerous in testing.
The mock passes, but production would fail!

Run this test to see how mocks can give false confidence.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockDatabase:
    """A mock database that doesn't enforce constraints"""
    
    def __init__(self):
        self.votes = []
        self.next_id = 1
    
    def execute(self, query, params=None):
        """Mock execute that doesn't enforce UNIQUE constraints"""
        if "INSERT INTO votes" in query:
            # Mock always allows inserts - no constraint checking!
            vote_id = self.next_id
            self.next_id += 1
            self.votes.append({
                'id': vote_id,
                'user_id': params[0],
                'choice': params[1]
            })
            return True
        elif "SELECT" in query:
            # Mock returns fake data
            return self.votes
        return True
    
    def commit(self):
        """Mock commit - always succeeds"""
        pass
    
    def rollback(self):
        """Mock rollback - does nothing"""
        pass

def submit_vote_mock(db, user_id, choice):
    """Submit vote using mock database"""
    try:
        # This will always succeed with mock!
        db.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, choice)
        )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

class TestVotingWithMock(unittest.TestCase):
    """Test voting functionality with mock database"""
    
    def setUp(self):
        """Set up test with mock database"""
        self.mock_db = MockDatabase()
    
    def test_first_vote_succeeds(self):
        """First vote should succeed"""
        result = submit_vote_mock(self.mock_db, "user1", "Python")
        self.assertTrue(result, "First vote should succeed")
        self.assertEqual(len(self.mock_db.votes), 1)
    
    def test_duplicate_vote_also_succeeds(self):
        """Duplicate vote also succeeds with mock - THIS IS THE PROBLEM!"""
        # First vote
        result1 = submit_vote_mock(self.mock_db, "user1", "Python")
        self.assertTrue(result1, "First vote should succeed")
        
        # Duplicate vote - mock allows it!
        result2 = submit_vote_mock(self.mock_db, "user1", "Python")
        self.assertTrue(result2, "Mock allows duplicate vote - BUG!")
        
        # Mock has 2 votes for same user - production would fail!
        self.assertEqual(len(self.mock_db.votes), 2)
    
    def test_multiple_duplicates_all_succeed(self):
        """Multiple duplicates all succeed with mock"""
        # Submit same vote 5 times
        for i in range(5):
            result = submit_vote_mock(self.mock_db, "user1", "Python")
            self.assertTrue(result, f"Vote {i+1} should succeed with mock")
        
        # Mock has 5 votes for same user - production constraint would prevent this!
        self.assertEqual(len(self.mock_db.votes), 5)
    
    def test_different_choices_same_user(self):
        """Same user voting different choices - mock allows all"""
        choices = ["Python", "JavaScript", "Go", "Rust"]
        
        for choice in choices:
            result = submit_vote_mock(self.mock_db, "user1", choice)
            self.assertTrue(result, f"Vote for {choice} should succeed with mock")
        
        # Mock allows 4 votes from same user - production would only allow 1!
        self.assertEqual(len(self.mock_db.votes), 4)

def demonstrate_mock_problem():
    """Demonstrate the mock problem clearly"""
    print("\n" + "="*60)
    print("❌ MOCK DATABASE TESTING - THE PROBLEM")
    print("="*60)
    
    mock_db = MockDatabase()
    
    print("\n🧪 Testing with Mock Database:")
    print("   - No constraint enforcement")
    print("   - No real SQL behavior")
    print("   - False confidence")
    
    print("\n📝 Test 1: First vote")
    result1 = submit_vote_mock(mock_db, "user1", "Python")
    print(f"   Result: {'✅ PASS' if result1 else '❌ FAIL'}")
    print(f"   Votes in mock: {len(mock_db.votes)}")
    
    print("\n📝 Test 2: Duplicate vote (should fail in production)")
    result2 = submit_vote_mock(mock_db, "user1", "Python")
    print(f"   Result: {'✅ PASS' if result2 else '❌ FAIL'}")
    print(f"   Votes in mock: {len(mock_db.votes)}")
    print("   ⚠️  PROBLEM: Mock allows duplicate vote!")
    
    print("\n📝 Test 3: Multiple duplicates")
    for i in range(3):
        result = submit_vote_mock(mock_db, "user1", "Python")
        print(f"   Vote {i+3}: {'✅ PASS' if result else '❌ FAIL'}")
    
    print(f"   Total votes in mock: {len(mock_db.votes)}")
    print("   ⚠️  PROBLEM: Same user voted 5 times!")
    
    print("\n💥 PRODUCTION IMPACT:")
    print("   - Users can vote multiple times")
    print("   - Data integrity compromised")
    print("   - Business logic violated")
    print("   - Security vulnerability")
    
    print("\n🎯 LESSON LEARNED:")
    print("   Mocks can lie! They don't test real database behavior.")
    print("   Use TestContainers for real database testing.")
    print("="*60)

if __name__ == '__main__':
    print("🧪 Running Mock Database Tests...")
    print("This demonstrates why mocks can be dangerous!")
    
    # Run the demonstration
    demonstrate_mock_problem()
    
    # Run unit tests
    print("\n🧪 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    print("\n💡 Next: Run test_with_testcontainers.py to see the solution!")
