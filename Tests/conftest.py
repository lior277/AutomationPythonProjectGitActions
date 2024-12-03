import pytest
from injector import Injector
from Infrastructure.Infra.dal.container.dependency_container import AppModule


def teardown():
    # Teardown code here
    print("Teardown: This will run once after all tests")


@pytest.fixture(scope='session', autouse=True)
def setup(request):
    # Setup code here
    print("Setup: This will run once before all tests")
    yield
    teardown()

@pytest.fixture(scope="session")
def injector() -> Injector:
    """Provide the dependency injector instance for tests."""
    return Injector([AppModule])
