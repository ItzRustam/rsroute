from .auth_tests import auth_test
from .logger import get_logger

# Added logger for colorfull logging in test cases
__all__ = ["auth_test", 'get_logger']