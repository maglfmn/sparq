import pytest

from app import create_app


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        help="Run the integration tests only in case of that command line (marked with marker @integration)",
    )


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getoption("--integration"):
        pytest.skip("need --integration option to run this test")


@pytest.fixture(scope="session")
def app():
    application = create_app()
    application.config["TESTING"] = True
    with application.app_context():
        yield application
