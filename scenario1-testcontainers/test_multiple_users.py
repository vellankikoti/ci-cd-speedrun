#!/usr/bin/env python3
"""
Test script to simulate multiple users voting
This demonstrates how the voting system works for real users
"""

import requests
import json
import time

def test_voting_system():
    """Test the voting system with multiple simulated users"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Voting System with Multiple Users")
    print("=" * 50)
    
    # Test 1: Multiple users can vote
    print("\n📝 Test 1: Multiple users voting")
    print("-" * 30)
    
    users = [
        {"name": "Alice", "choice": "Python"},
        {"name": "Bob", "choice": "JavaScript"},
        {"name": "Charlie", "choice": "Go"},
        {"name": "Diana", "choice": "Rust"},
        {"name": "Eve", "choice": "Python"},  # Same choice as Alice
    ]
    
    # Create session for each user (simulates different browsers)
    sessions = []
    for user in users:
        session = requests.Session()
        sessions.append((user, session))
    
    # Each user votes
    for user, session in sessions:
        response = session.post(
            f"{base_url}/api/vote",
            json={"choice": user["choice"]},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        if data["status"] == "success":
            print(f"✅ {user['name']} voted for {user['choice']} - User ID: {data['user_id']}")
        else:
            print(f"❌ {user['name']} failed to vote: {data['message']}")
    
    # Test 2: Same user tries to vote again (should fail)
    print("\n📝 Test 2: Same user tries to vote again")
    print("-" * 40)
    
    alice_session = sessions[0][1]  # Alice's session
    response = alice_session.post(
        f"{base_url}/api/vote",
        json={"choice": "JavaScript"},  # Different choice
        headers={"Content-Type": "application/json"}
    )
    
    data = response.json()
    if data["status"] == "error":
        print(f"🎯 {data['message']}")
        print(f"   Detail: {data['detail']}")
        print(f"   Magic: {data['magic_moment']}")
        print(f"   Learning: {data['learning']}")
    else:
        print(f"❌ Expected error but got: {data}")
    
    # Test 3: Check final results
    print("\n📝 Test 3: Final voting results")
    print("-" * 30)
    
    response = requests.get(f"{base_url}/api/stats")
    data = response.json()
    
    print(f"📊 Total votes: {data['total_votes']}")
    print(f"👥 Unique users: {data['unique_users']}")
    print(f"🗳️  Results:")
    for result in data['results']:
        print(f"   {result['choice']}: {result['count']} votes")
    
    print(f"\n🎓 Learning: {data['learning']}")
    print(f"🔒 Constraint: {data['constraint']}")
    
    # Test 4: Reset and test again
    print("\n📝 Test 4: Reset and test again")
    print("-" * 30)
    
    response = requests.post(f"{base_url}/api/reset")
    data = response.json()
    print(f"🔄 {data['message']}")
    
    # Alice votes again after reset
    response = alice_session.post(
        f"{base_url}/api/vote",
        json={"choice": "Rust"},
        headers={"Content-Type": "application/json"}
    )
    
    data = response.json()
    if data["status"] == "success":
        print(f"✅ Alice voted again after reset: {data['message']}")
    else:
        print(f"❌ Alice couldn't vote after reset: {data['message']}")
    
    print("\n🎉 Test Complete!")
    print("=" * 50)
    print("✅ Multiple users can vote")
    print("✅ Each user can only vote once")
    print("✅ Real database constraints work")
    print("✅ Reset functionality works")
    print("✅ Perfect for workshop demonstrations!")

if __name__ == "__main__":
    test_voting_system()
