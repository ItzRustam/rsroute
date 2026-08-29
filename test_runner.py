# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

import sys

from tests import auth_test
from tests import get_logger
from tests import api_config_test

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

def api_config_testing():
    logger.info("Running API config TestCases.")

    logger.info("Test Case #1 - Invalid Provider")
    val, result = api_config_test(provider="qwen", key="my_key404xd")
    logger.debug(f"case #1 Result - {result}")

    logger.info("Test Case #2 - Groq Provider") 
    val, result = api_config_test(provider="groq", key="my_key_groq_xd")
    logger.debug(f"case #2 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #2 `Groq Provider` Failed.")
        return False

    logger.info("Test Case #3 - OpenAI Provider") 
    val, result = api_config_test(provider="openai", key="my_key_openai_xd")
    logger.debug(f"case #3 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #3 `OpenAI Provider` Failed.")
        return False

    logger.info("Test Case #4 - Gemini Provider") 
    val, result = api_config_test(provider="gemini", key="my_key_gemini_xd")
    logger.debug(f"case #4 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #4 `Gemini Provider` Failed.")
        return False

    logger.info("Test Case #5 - Huggingface Provider") 
    val, result = api_config_test(provider="hf", key="my_key_hf_xd")
    logger.debug(f"case #5 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #5 `Huggingface Provider` Failed.")
        return False

    logger.info("Test Case #6 - Mistral Provider") 
    val, result = api_config_test(provider="mistral", key="my_key_mistral_xd")
    logger.debug(f"case #6 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #6 `Mistral Provider` Failed.")
        return False

    logger.info("Test Case #7 - OpenRouter Provider") 
    val, result = api_config_test(provider="openrouter", key="my_key_or_xd")
    logger.debug(f"case #7 Result - {result}")
    if val:
        pass
    else:
        logger.error("Test Case #7 `OpenRouter Provider` Failed.")
        return False

    logger.info("============ All Test Case Passed 7/7 =================")
    return True
    


def main():
    results = []
    results.append(auth_testing()) # Auth Test Case
    results.append(api_config_testing()) # API config Test Case

    return all(results) # Return False if any Test Case Failed
    


if __name__ == "__main__":
    sys.exit(0 if main() else 1)