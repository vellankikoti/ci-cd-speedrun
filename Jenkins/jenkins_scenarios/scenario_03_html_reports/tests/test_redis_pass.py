"""
Scenario 03: HTML Reports Chaos - Redis Cache Tests (PASS)

These tests demonstrate proper Redis caching patterns using testcontainers
that should always pass with a healthy Redis instance.
"""

import pytest
import redis
import json
import time
from testcontainers.redis import RedisContainer


class TestRedisPass:
    """Test Redis cache scenarios that should pass"""

    def test_redis_container_startup_and_connection(self):
        """Test that Redis container starts and accepts connections"""
        with RedisContainer("redis:7") as redis_container:
            # Get connection details
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create Redis client
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Test basic connection
            assert client.ping() is True, "Redis should respond to ping"
            
            # Test basic set/get operations
            client.set("test_key", "test_value")
            value = client.get("test_key")
            assert value == "test_value", "Should be able to set and get values"

    def test_redis_string_operations(self):
        """Test Redis string data type operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Basic string operations
            client.set("counter", 0)
            assert client.get("counter") == "0", "Initial counter should be 0"
            
            # Increment operations
            new_value = client.incr("counter")
            assert new_value == 1, "Counter should increment to 1"
            
            # Increment by specific amount
            new_value = client.incr("counter", 5)
            assert new_value == 6, "Counter should increment by 5 to reach 6"
            
            # Decrement operations
            new_value = client.decr("counter")
            assert new_value == 5, "Counter should decrement to 5"
            
            # String append
            client.set("message", "Hello")
            length = client.append("message", " World")
            assert length == 11, "Appended string should be 11 characters long"
            assert client.get("message") == "Hello World", "Message should be concatenated"
            
            # Multiple set/get
            mapping = {"key1": "value1", "key2": "value2", "key3": "value3"}
            client.mset(mapping)
            
            values = client.mget(["key1", "key2", "key3"])
            assert values == ["value1", "value2", "value3"], "Multiple get should return all values"

    def test_redis_hash_operations(self):
        """Test Redis hash data type operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            hash_key = "user:1001"
            
            # Set hash fields
            client.hset(hash_key, "name", "John Doe")
            client.hset(hash_key, "email", "john@example.com")
            client.hset(hash_key, "age", "30")
            
            # Get single hash field
            name = client.hget(hash_key, "name")
            assert name == "John Doe", "Hash field 'name' should match"
            
            # Get multiple hash fields
            user_data = client.hmget(hash_key, ["name", "email", "age"])
            assert user_data == ["John Doe", "john@example.com", "30"], "Multiple hash fields should match"
            
            # Get all hash fields
            all_data = client.hgetall(hash_key)
            expected_data = {"name": "John Doe", "email": "john@example.com", "age": "30"}
            assert all_data == expected_data, "All hash data should match"
            
            # Check if field exists
            assert client.hexists(hash_key, "name") is True, "Field 'name' should exist"
            assert client.hexists(hash_key, "nonexistent") is False, "Field 'nonexistent' should not exist"
            
            # Get hash length
            length = client.hlen(hash_key)
            assert length == 3, "Hash should have 3 fields"
            
            # Delete hash field
            client.hdel(hash_key, "age")
            assert client.hexists(hash_key, "age") is False, "Field 'age' should be deleted"
            assert client.hlen(hash_key) == 2, "Hash should have 2 fields after deletion"

    def test_redis_list_operations(self):
        """Test Redis list data type operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            list_key = "task_queue"
            
            # Push elements to the right (append)
            client.rpush(list_key, "task1", "task2", "task3")
            
            # Get list length
            length = client.llen(list_key)
            assert length == 3, "List should have 3 elements"
            
            # Get range of elements
            tasks = client.lrange(list_key, 0, -1)  # Get all elements
            assert tasks == ["task1", "task2", "task3"], "List elements should match"
            
            # Push to the left (prepend)
            client.lpush(list_key, "urgent_task")
            
            # Pop from left (FIFO-like behavior)
            urgent_task = client.lpop(list_key)
            assert urgent_task == "urgent_task", "Should pop the urgent task first"
            
            # Pop from right (LIFO-like behavior)
            last_task = client.rpop(list_key)
            assert last_task == "task3", "Should pop the last task"
            
            # Get element by index
            first_task = client.lindex(list_key, 0)
            assert first_task == "task1", "First element should be task1"
            
            # Set element by index
            client.lset(list_key, 1, "modified_task2")
            modified_task = client.lindex(list_key, 1)
            assert modified_task == "modified_task2", "Task should be modified"

    def test_redis_set_operations(self):
        """Test Redis set data type operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            set_key1 = "skills:developer1"
            set_key2 = "skills:developer2"
            
            # Add members to sets
            client.sadd(set_key1, "python", "javascript", "sql", "docker")
            client.sadd(set_key2, "python", "java", "sql", "kubernetes")
            
            # Check set membership
            assert client.sismember(set_key1, "python") is True, "Developer1 should have python skill"
            assert client.sismember(set_key1, "java") is False, "Developer1 should not have java skill"
            
            # Get set size
            size1 = client.scard(set_key1)
            assert size1 == 4, "Developer1 should have 4 skills"
            
            # Get all members
            skills1 = client.smembers(set_key1)
            expected_skills1 = {"python", "javascript", "sql", "docker"}
            assert skills1 == expected_skills1, "Developer1 skills should match"
            
            # Set operations
            # Intersection (common skills)
            common_skills = client.sinter(set_key1, set_key2)
            assert common_skills == {"python", "sql"}, "Common skills should be python and sql"
            
            # Union (all skills)
            all_skills = client.sunion(set_key1, set_key2)
            expected_all_skills = {"python", "javascript", "sql", "docker", "java", "kubernetes"}
            assert all_skills == expected_all_skills, "Union should include all skills"
            
            # Difference (skills unique to developer1)
            unique_skills1 = client.sdiff(set_key1, set_key2)
            assert unique_skills1 == {"javascript", "docker"}, "Developer1 unique skills should match"
            
            # Remove member
            client.srem(set_key1, "docker")
            assert client.sismember(set_key1, "docker") is False, "Docker should be removed"

    def test_redis_sorted_set_operations(self):
        """Test Redis sorted set data type operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            leaderboard_key = "game_scores"
            
            # Add members with scores
            client.zadd(leaderboard_key, {"player1": 1000, "player2": 1500, "player3": 800, "player4": 2000})
            
            # Get rank (0-based, lowest to highest score)
            rank = client.zrank(leaderboard_key, "player2")
            assert rank == 2, "Player2 should be rank 2 (third place from bottom)"
            
            # Get reverse rank (0-based, highest to lowest score)
            rev_rank = client.zrevrank(leaderboard_key, "player2")
            assert rev_rank == 1, "Player2 should be rank 1 (second place from top)"
            
            # Get score
            score = client.zscore(leaderboard_key, "player2")
            assert score == 1500.0, "Player2 score should be 1500"
            
            # Get range by rank (top 3 players)
            top_players = client.zrevrange(leaderboard_key, 0, 2, withscores=True)
            expected_top = [("player4", 2000.0), ("player2", 1500.0), ("player1", 1000.0)]
            assert top_players == expected_top, "Top 3 players should match"
            
            # Get range by score
            mid_range_players = client.zrangebyscore(leaderboard_key, 900, 1600, withscores=True)
            expected_mid = [("player1", 1000.0), ("player2", 1500.0)]
            assert mid_range_players == expected_mid, "Mid-range players should match"
            
            # Increment score
            new_score = client.zincrby(leaderboard_key, 500, "player3")
            assert new_score == 1300.0, "Player3 new score should be 1300"
            
            # Count members in score range
            count = client.zcount(leaderboard_key, 1000, 2000)
            assert count == 3, "Should have 3 players in score range 1000-2000"

    def test_redis_expiration_and_ttl(self):
        """Test Redis key expiration and TTL functionality"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set key with expiration
            client.setex("session:user123", 5, "session_data")  # 5 seconds TTL
            
            # Check TTL
            ttl = client.ttl("session:user123")
            assert 4 <= ttl <= 5, "TTL should be around 5 seconds"
            
            # Key should exist
            assert client.exists("session:user123") == 1, "Session key should exist"
            
            # Set expiration on existing key
            client.set("persistent_key", "some_data")
            client.expire("persistent_key", 3)  # 3 seconds TTL
            
            ttl = client.ttl("persistent_key")
            assert 2 <= ttl <= 3, "TTL should be around 3 seconds"
            
            # Remove expiration
            client.persist("persistent_key")
            ttl = client.ttl("persistent_key")
            assert ttl == -1, "Key should have no expiration (-1)"
            
            # Test key expiration by waiting
            client.setex("temp_key", 1, "temp_value")  # 1 second TTL
            assert client.exists("temp_key") == 1, "Temp key should exist initially"
            
            time.sleep(1.5)  # Wait for expiration
            assert client.exists("temp_key") == 0, "Temp key should expire after 1 second"

    def test_redis_json_data_storage(self):
        """Test storing and retrieving JSON data in Redis"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Store complex data structures as JSON
            user_profile = {
                "user_id": 12345,
                "username": "john_doe",
                "email": "john@example.com",
                "preferences": {
                    "theme": "dark",
                    "notifications": True,
                    "language": "en"
                },
                "last_login": "2024-01-01T12:00:00Z",
                "roles": ["user", "editor"]
            }
            
            # Serialize and store
            client.set("user_profile:12345", json.dumps(user_profile))
            
            # Retrieve and deserialize
            stored_json = client.get("user_profile:12345")
            stored_profile = json.loads(stored_json)
            
            assert stored_profile == user_profile, "Stored and retrieved profile should match"
            assert stored_profile["user_id"] == 12345, "User ID should be preserved"
            assert stored_profile["preferences"]["theme"] == "dark", "Nested data should be preserved"
            assert "editor" in stored_profile["roles"], "Array data should be preserved"

    def test_redis_pipeline_operations(self):
        """Test Redis pipeline for batch operations"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Create pipeline
            pipe = client.pipeline()
            
            # Add multiple operations to pipeline
            pipe.set("batch_key1", "value1")
            pipe.set("batch_key2", "value2")
            pipe.incr("batch_counter")
            pipe.lpush("batch_list", "item1", "item2")
            pipe.sadd("batch_set", "member1", "member2")
            
            # Execute all operations at once
            results = pipe.execute()
            
            # Verify results
            assert results[0] is True, "First set operation should succeed"
            assert results[1] is True, "Second set operation should succeed"
            assert results[2] == 1, "Counter should be incremented to 1"
            assert results[3] == 2, "List should have 2 items"
            assert results[4] == 2, "Set should have 2 members"
            
            # Verify data was actually stored
            assert client.get("batch_key1") == "value1", "Batch key1 should be stored"
            assert client.get("batch_key2") == "value2", "Batch key2 should be stored"
            assert client.get("batch_counter") == "1", "Batch counter should be 1"
            assert client.llen("batch_list") == 2, "Batch list should have 2 items"
            assert client.scard("batch_set") == 2, "Batch set should have 2 members"

    def test_redis_pub_sub_basic(self):
        """Test Redis publish/subscribe functionality"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create separate clients for publisher and subscriber
            publisher = redis.Redis(host=host, port=port, decode_responses=True)
            subscriber = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Create pubsub object
            pubsub = subscriber.pubsub()
            
            # Subscribe to a channel
            pubsub.subscribe("test_channel")
            
            # Skip the subscription confirmation message
            subscription_message = pubsub.get_message(timeout=1)
            assert subscription_message is not None, "Should receive subscription confirmation"
            assert subscription_message["type"] == "subscribe", "Message type should be subscribe"
            
            # Publish a message
            publisher.publish("test_channel", "Hello Redis!")
            
            # Receive the message
            message = pubsub.get_message(timeout=5)
            assert message is not None, "Should receive published message"
            assert message["type"] == "message", "Message type should be message"
            assert message["channel"] == "test_channel", "Channel should match"
            assert message["data"] == "Hello Redis!", "Message data should match"
            
            # Clean up
            pubsub.unsubscribe("test_channel")
            pubsub.close()

    def test_redis_connection_pooling(self):
        """Test Redis connection pooling"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create connection pool
            pool = redis.ConnectionPool(
                host=host,
                port=port,
                max_connections=5,
                decode_responses=True
            )
            
            # Create multiple clients using the same pool
            clients = []
            for i in range(3):
                client = redis.Redis(connection_pool=pool)
                clients.append(client)
                
                # Test each client works
                client.set(f"pool_test_{i}", f"value_{i}")
                value = client.get(f"pool_test_{i}")
                assert value == f"value_{i}", f"Client {i} should work correctly"
            
            # Verify pool statistics
            assert len(pool._created_connections) <= 5, "Pool should not exceed max connections"
            
            # Clean up
            for client in clients:
                client.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])