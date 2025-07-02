import pytest
import time
import random
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

# Colors for log output
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def chaos_delay(max_seconds=3):
    """
    Introduce a random delay to simulate chaos in test execution.
    """
    delay = random.randint(0, max_seconds)
    if delay > 0:
        print(f"{YELLOW}💥 Chaos delay introduced... sleeping {delay} seconds.{RESET}")
        time.sleep(delay)


def test_mongodb_version():
    """
    ✅ Test Case 1 - Check MongoDB server version
    """
    print(f"{CYAN}✨ 🚀 Starting test: Check MongoDB version{RESET}")
    chaos_delay()

    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        version = client.server_info()["version"]
        print(f"{GREEN}✨ MongoDB version fetched: {version}{RESET}")
        assert version.startswith("7.")

    print(f"{GREEN}✅ MongoDB version test passed!{RESET}\n")


def test_insert_and_find():
    """
    ✅ Test Case 2 - Insert one document and find it
    """
    print(f"{CYAN}✨ 🚀 Starting test: Insert and Find One Document{RESET}")
    chaos_delay()

    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "Alice"})
        result = db.users.find_one({"name": "Alice"})
        assert result["name"] == "Alice"

    print(f"{GREEN}✅ Insert and Find One Document test passed!{RESET}\n")


def test_multiple_documents():
    """
    ✅ Test Case 3 - Insert multiple documents and count
    """
    print(f"{CYAN}✨ 🚀 Starting test: Insert Multiple Documents and Count{RESET}")
    chaos_delay()

    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_many([
            {"name": "Bob"},
            {"name": "Charlie"},
        ])
        count = db.users.count_documents({})
        print(f"{GREEN}✨ Total documents in collection: {count}{RESET}")
        assert count == 2

    print(f"{GREEN}✅ Insert Multiple Documents and Count test passed!{RESET}\n")


def test_update_document():
    """
    ✅ Test Case 4 - Update a document field
    """
    print(f"{CYAN}✨ 🚀 Starting test: Update a Document Field{RESET}")
    chaos_delay()

    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "David"})
        db.users.update_one({"name": "David"}, {"$set": {"name": "Daniel"}})
        result = db.users.find_one({"name": "Daniel"})
        assert result is not None

    print(f"{GREEN}✅ Update a Document Field test passed!{RESET}\n")


def test_delete_document():
    """
    ✅ Test Case 5 - Delete a document and verify
    """
    print(f"{CYAN}✨ 🚀 Starting test: Delete a Document and Verify{RESET}")
    chaos_delay()

    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "Eve"})
        db.users.delete_one({"name": "Eve"})
        result = db.users.find_one({"name": "Eve"})
        assert result is None

    print(f"{GREEN}✅ Delete a Document and Verify test passed!{RESET}\n")
