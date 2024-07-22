import pytest
from waf.db_query_wrapper import execute_wrapper
from waf.middleware import SQLInjectionMiddleware
from waf.rate_limit_middleware import RateLimitMiddleware
from unittest.mock import patch, MagicMock


@pytest.fixture
def setup():
    # Setup code for the tests
    yield
    # Teardown code for the tests


# Mocking the original execute function to prevent actual database queries
@patch('waf.db_query_wrapper.execute_wrapper', return_value=True)
def test_execute_wrapper_with_prohibited_pattern(mock_execute):
    # Assuming 'DROP TABLE' is a prohibited pattern
    prohibited_sql = "DROP TABLE;"
    with pytest.raises(Exception) as excinfo:
        execute_wrapper(prohibited_sql)
    assert "prohibited pattern detected" in str(excinfo.value).lower()
    mock_execute.assert_not_called()

@patch('waf.db_query_wrapper.execute_wrapper', return_value=True)
def test_execute_wrapper_without_prohibited_pattern(mock_execute):
    # A safe query without prohibited patterns
    safe_sql = "SELECT * FROM;"
    assert execute_wrapper(safe_sql) is True
    mock_execute.assert_called_once_with(safe_sql, None)

def test_custom_middleware():
    # Test the custom_middleware function
    request = MockRequest()
    response = SQLInjectionMiddleware(request)
    assert response is not None

def test_rate_limit_middleware():
    # Test the rate_limit middleware
    request = MockRequest()
    response = RateLimitMiddleware(request)
    assert response is not None

class MockRequest:
    # Mock request class for testing purposes
    pass

