import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient


def test_mongodb_version():
    """
    ✅ Test Case 1 - Check MongoDB server version
    """
    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        version = client.server_info()["version"]
        print("MongoDB version:", version)
        assert version.startswith("7.")


def test_insert_and_find():
    """
    ✅ Test Case 2 - Insert one document and find it
    """
    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "Alice"})
        result = db.users.find_one({"name": "Alice"})
        assert result["name"] == "Alice"


def test_multiple_documents():
    """
    ✅ Test Case 3 - Insert multiple documents and count
    """
    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_many([
            {"name": "Bob"},
            {"name": "Charlie"},
        ])
        count = db.users.count_documents({})
        assert count == 2


def test_update_document():
    """
    ✅ Test Case 4 - Update a document field
    """
    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "David"})
        db.users.update_one({"name": "David"}, {"$set": {"name": "Daniel"}})
        result = db.users.find_one({"name": "Daniel"})
        assert result is not None


def test_delete_document():
    """
    ✅ Test Case 5 - Delete a document and verify
    """
    with MongoDbContainer("mongo:7.0") as mongo:
        client = MongoClient(mongo.get_connection_url())
        db = client.test
        db.users.insert_one({"name": "Eve"})
        db.users.delete_one({"name": "Eve"})
        result = db.users.find_one({"name": "Eve"})
        assert result is None
