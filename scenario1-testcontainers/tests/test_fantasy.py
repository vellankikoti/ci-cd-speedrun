#!/usr/bin/env python3
"""
❌ THE LIE: Fantasy Tests with Mocks
=====================================

These tests pass with flying colors.
They're fast. They're green. They're WRONG.

This is what happens when tests live in fantasy land.
"""

import pytest


class MockDatabase:
    """
    A mock database that simulates success.
    The problem: It doesn't enforce ANY constraints.
    """

    def __init__(self):
        self.votes = []

    def insert_vote(self, user_id, choice):
        """
        Always succeeds - no constraint checking!
        In production, this would be a PostgreSQL database with UNIQUE constraints.
        But mocks don't know about that.
        """
        self.votes.append({'user_id': user_id, 'choice': choice})
        return True  # Always returns success!

    def get_votes_count(self):
        return len(self.votes)


def test_single_vote_works():
    """✅ This test passes"""
    db = MockDatabase()

    result = db.insert_vote("user123", "Python")

    assert result is True
    assert db.get_votes_count() == 1


def test_duplicate_vote_should_fail():
    """
    ❌ THIS TEST PASSES BUT IT'S A LIE!

    In production:
    - PostgreSQL has UNIQUE(user_id) constraint
    - Second vote would fail with IntegrityError
    - Users can only vote once

    In this test:
    - Mock has NO constraints
    - Second vote succeeds
    - Test passes
    - Bug ships to production
    """
    db = MockDatabase()

    # First vote - should work
    result1 = db.insert_vote("user123", "Python")
    assert result1 is True
    assert db.get_votes_count() == 1

    # Second vote - SHOULD FAIL but doesn't!
    result2 = db.insert_vote("user123", "Python")  # Same user!
    assert result2 is True  # ⚠️ This passes but it's WRONG!
    assert db.get_votes_count() == 2  # ⚠️ Two votes from one user!

    # ❌ BUG: The mock allowed duplicate votes
    # ❌ In production: Users could vote unlimited times
    # ❌ Business logic broken
    # ❌ Data integrity compromised


def test_unlimited_votes_all_succeed():
    """
    💥 THE DISASTER: Unlimited votes from same user

    This test demonstrates the catastrophic failure.
    All votes succeed. Test is green. Production is broken.
    """
    db = MockDatabase()

    user_id = "cheater123"

    # Vote 100 times as the same user
    for i in range(100):
        result = db.insert_vote(user_id, "Python")
        assert result is True  # All succeed!

    # Mock allowed 100 votes from one user!
    assert db.get_votes_count() == 100

    # ❌ In production with UNIQUE constraint:
    #    - First vote: SUCCESS
    #    - Votes 2-100: IntegrityError
    #    - Final count: 1 vote
    #
    # ❌ But this test says everything is fine!


# ==============================================================================
# THE PROBLEM IN SUMMARY
# ==============================================================================

"""
These tests give FALSE CONFIDENCE:

1. Fast: ✅ (milliseconds)
2. Green: ✅ (all pass)
3. Correct: ❌ (lies!)

Why they fail in production:
- No database constraints (UNIQUE, FOREIGN KEY, CHECK)
- No connection errors or timeouts
- No transaction conflicts
- No real database behavior

The solution: TestContainers
- Real database with real constraints
- Tests that actually prove correctness
- Production parity

Run the REAL tests: `pytest tests/test_reality.py -v`
"""
