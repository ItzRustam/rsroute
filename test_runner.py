import sys

from tests import auth_test
from tests import get_logger

logger = get_logger(__name__)


def auth_testing():
    logger.info("Running auth test suite")

    logger.info("Test Case #1 - No master_key")
    result = auth_test()
    logger.debug(f"case #1 Result: {result}")

    logger.info("Test Case #2 - Invalid suffix, no `RSRoute_` at start")
    result = auth_test(master_key="blablabla")
    logger.debug(f"case #2 Result: {result}")

    logger.info("Test Case #3 - Invalid key/Token")
    result = auth_test(master_key="RSRoute_invalid_token")
    logger.debug(f"case #3 Result: {result}")

    logger.info("Test Case #4 - Valid master key")
    result = auth_test(master_key="RSRoute_my_key")

    if result == "Auth Done.":
        logger.info("Test Case #4 Passed.")
        return True

    logger.error("Test Case #4 Failed with correct master key.")
    return False


def main():
    return auth_testing()


if __name__ == "__main__":
    sys.exit(0 if main() else 1)