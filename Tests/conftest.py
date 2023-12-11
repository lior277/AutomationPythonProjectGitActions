import pytest


def teardown():
    # Teardown code here
    print("Teardown: This will run once after all tests")


@pytest.fixture(scope='session', autouse=True)
def setup(request):
    # Setup code here
    print("Setup: This will run once before all tests")
    yield
    teardown()
