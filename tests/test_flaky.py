import random

def test_flaky():
    """
    Chaos Agent's sabotage:
    This test randomly fails.
    """
    assert random.choice([True, False])

