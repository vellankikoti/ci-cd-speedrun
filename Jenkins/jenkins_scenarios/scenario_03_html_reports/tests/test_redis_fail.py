"""
Scenario 03: HTML Reports Chaos - Redis Cache Tests (FAIL)

These tests simulate real-world Redis cache failures that should
always fail to demonstrate common enterprise caching problems.
"""

import pytest
import redis
import json
import time
from testcontainers.redis import RedisContainer
from redis.exceptions import ConnectionError, TimeoutError, ResponseError


class TestRedisFail:
    """Test Redis cache scenarios that should fail"""

    def test_redis_connection_refused(self):
        """Test Redis connection when server is not available"""
        try:
            # Try to connect to non-existent Redis server
            client = redis.Redis(host='192.0.2.1', port=6379, socket_timeout=1)  # Non-routable IP
            client.ping()
            assert False, "Should not be able to connect to non-existent Redis server"
        except ConnectionError:
            # Expected error, but test should fail anyway
            assert False, "Connection refused as expected, but test designed to fail"

    def test_redis_authentication_failure(self):
        """Test Redis connection with wrong authentication"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Try to connect with wrong password
            try:
                client = redis.Redis(host=host, port=port, password="wrong_password", decode_responses=True)
                client.ping()
                assert False, "Should not authenticate with wrong password"
            except Exception:
                # Expected authentication failure
                assert False, "Authentication failed as expected, but test designed to fail"

    def test_redis_memory_exhaustion(self):
        """Test Redis behavior when memory is exhausted"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            try:
                # Try to fill up Redis memory with large data
                large_data = "x" * 1024 * 1024  # 1MB string
                
                # Attempt to store many large objects
                for i in range(1000):  # This might exhaust memory
                    key = f"large_data_{i}"
                    client.set(key, large_data)
                
                # If we reach here without memory error, test should fail
                assert False, "Should have encountered memory exhaustion"
                
            except Exception:
                # Memory exhaustion or other error
                assert False, "Memory error as expected, but test designed to fail"

    def test_redis_key_not_found_operations(self):
        """Test operations on non-existent keys that should fail"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Try to perform operations on non-existent keys
            try:
                # This will return None, but we expect it to exist
                value = client.get("nonexistent_key")
                assert value is not None, "Key should exist but doesn't"
                
                # This will return 0, but we expect the key to exist
                length = client.llen("nonexistent_list")
                assert length > 0, "List should have elements but doesn't exist"
                
                # This will return empty set, but we expect members
                members = client.smembers("nonexistent_set")
                assert len(members) > 0, "Set should have members but doesn't exist"
                
            except Exception:
                assert False, "Key operations failed as expected, but test designed to fail"

    def test_redis_data_type_mismatch_operations(self):
        """Test operations on wrong data types"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set a string value
            client.set("string_key", "just_a_string")
            
            try:
                # Try to perform list operations on string key
                client.lpush("string_key", "list_item")
                assert False, "Should not be able to perform list operations on string key"
            except ResponseError:
                # Expected type error
                assert False, "Type mismatch error as expected, but test designed to fail"

    def test_redis_expired_key_access(self):
        """Test accessing keys that have expired"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set key with very short expiration
            client.setex("short_lived_key", 1, "temporary_value")
            
            # Wait for expiration
            time.sleep(1.5)
            
            # Try to access expired key
            value = client.get("short_lived_key")
            assert value is not None, "Key should still exist but has expired"
            assert value == "temporary_value", "Expired key should retain its value"

    def test_redis_pipeline_partial_failure(self):
        """Test pipeline operations with partial failures"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set up initial data
            client.set("existing_string", "string_value")
            
            # Create pipeline with mixed valid and invalid operations
            pipe = client.pipeline()
            pipe.set("valid_key1", "value1")  # Valid
            pipe.lpush("existing_string", "item")  # Invalid - wrong type
            pipe.set("valid_key2", "value2")  # Valid
            
            try:
                results = pipe.execute()
                # If pipeline succeeds, test should fail
                assert False, "Pipeline should fail due to type mismatch"
            except ResponseError:
                # Expected pipeline failure
                assert False, "Pipeline failed as expected, but test designed to fail"

    def test_redis_connection_timeout(self):
        """Test Redis operations with connection timeout"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create client with very short timeout
            client = redis.Redis(
                host=host, 
                port=port, 
                socket_timeout=0.001,  # Very short timeout
                decode_responses=True
            )
            
            try:
                # This might timeout due to very short timeout setting
                client.set("timeout_test", "value")
                value = client.get("timeout_test")
                assert value == "value", "Operation should complete within timeout"
                
                # If we reach here, test should fail
                assert False, "Operations should timeout with such short timeout setting"
                
            except TimeoutError:
                # Expected timeout
                assert False, "Timeout occurred as expected, but test designed to fail"

    def test_redis_pub_sub_no_subscribers(self):
        """Test publishing to channels with no subscribers"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Publish to channel with no subscribers
            subscribers_count = client.publish("empty_channel", "message_to_nowhere")
            
            # This should return 0 subscribers, but we expect subscribers
            assert subscribers_count > 0, "Should have subscribers for the message"
            assert False, "No subscribers as expected, but test designed to fail"

    def test_redis_lua_script_error(self):
        """Test Redis Lua script execution errors"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Lua script with syntax error
            buggy_script = """
                local key = KEYS[1]
                local value = ARGV[1]
                -- This script has intentional syntax error
                redis.call('SET', key, value
                -- Missing closing parenthesis above
                return redis.call('GET', key)
            """
            
            try:
                result = client.eval(buggy_script, 1, "test_key", "test_value")
                assert result == "test_value", "Script should execute successfully"
                assert False, "Buggy Lua script should not execute successfully"
            except ResponseError:
                # Expected script error
                assert False, "Lua script error as expected, but test designed to fail"

    def test_redis_transaction_watch_conflict(self):
        """Test Redis WATCH/MULTI/EXEC transaction conflicts"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create two separate clients to simulate concurrent access
            client1 = redis.Redis(host=host, port=port, decode_responses=True)
            client2 = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set initial value
            client1.set("watched_key", "initial_value")
            
            # Client 1 starts watching the key
            client1.watch("watched_key")
            
            # Client 2 modifies the watched key (this should cause conflict)
            client2.set("watched_key", "modified_by_client2")
            
            # Client 1 tries to execute transaction
            pipe = client1.pipeline()
            pipe.multi()
            pipe.set("watched_key", "modified_by_client1")
            
            try:
                results = pipe.execute()
                # If transaction succeeds despite conflict, test should fail
                if results is not None:
                    assert False, "Transaction should be aborted due to watch conflict"
                else:
                    # Transaction was aborted as expected
                    assert False, "Transaction conflict detected as expected, but test designed to fail"
            except Exception:
                assert False, "Transaction error as expected, but test designed to fail"

    def test_redis_max_connections_exceeded(self):
        """Test Redis max connections limit"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Try to create many connections to exhaust the limit
            connections = []
            try:
                for i in range(100):  # Try to create many connections
                    client = redis.Redis(
                        host=host, 
                        port=port, 
                        decode_responses=True,
                        connection_pool=redis.ConnectionPool(
                            host=host, 
                            port=port, 
                            max_connections=1  # Very limited pool
                        )
                    )
                    connections.append(client)
                    client.ping()  # Force connection
                
                # If we reach here, test should fail
                assert False, "Should not be able to create unlimited connections"
                
            except Exception:
                # Expected connection limit error
                assert False, "Connection limit exceeded as expected, but test designed to fail"
            finally:
                # Clean up connections
                for conn in connections:
                    try:
                        conn.close()
                    except:
                        pass

    def test_redis_corrupted_data_retrieval(self):
        """Test retrieval of corrupted data from Redis"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Store valid JSON data
            valid_data = {"user_id": 123, "name": "John", "active": True}
            client.set("user_data", json.dumps(valid_data))
            
            # Simulate data corruption by overwriting with invalid JSON
            client.set("user_data", '{"user_id": 123, "name": "John", "active":')  # Incomplete JSON
            
            # Try to retrieve and parse the corrupted data
            try:
                stored_data = client.get("user_data")
                parsed_data = json.loads(stored_data)
                
                # This should fail due to invalid JSON
                assert parsed_data["user_id"] == 123, "Should parse user_id correctly"
                assert parsed_data["name"] == "John", "Should parse name correctly"
                assert parsed_data["active"] is True, "Should parse active status correctly"
                
            except json.JSONDecodeError:
                # Expected JSON parsing error
                assert False, "JSON parsing failed as expected, but test designed to fail"

    def test_redis_key_collision_and_overwrites(self):
        """Test unintended key collisions and data overwrites"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Set important data
            client.set("important_config", "critical_production_setting")
            
            # Simulate accidental overwrite with different data type
            client.lpush("important_config", "list_item1", "list_item2")
            
            # Try to retrieve as string (original type)
            try:
                config_value = client.get("important_config")
                assert config_value == "critical_production_setting", "Config should retain original value"
                assert False, "Key type should not have changed from string to list"
            except Exception:
                # Expected type error or data loss
                assert False, "Data corruption detected as expected, but test designed to fail"

    def test_redis_network_partition_simulation(self):
        """Test Redis behavior during network partition"""
        with RedisContainer("redis:7") as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(6379)
            
            # Create client with short timeouts
            client = redis.Redis(
                host=host, 
                port=port, 
                socket_timeout=0.1,
                socket_connect_timeout=0.1,
                decode_responses=True
            )
            
            # Store initial data
            client.set("network_test", "initial_value")
            
            # Simulate network issues by connecting to wrong port
            problematic_client = redis.Redis(
                host=host, 
                port=9999,  # Wrong port to simulate network issue
                socket_timeout=0.1,
                decode_responses=True
            )
            
            try:
                # This should fail due to wrong port
                value = problematic_client.get("network_test")
                assert value == "initial_value", "Should retrieve value despite network issues"
                assert False, "Network operation should fail"
            except Exception:
                # Expected network error
                assert False, "Network error as expected, but test designed to fail"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])