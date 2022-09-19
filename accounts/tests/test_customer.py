import pytest


@pytest.fixture
def fixture1():
    print(True)
    return 1