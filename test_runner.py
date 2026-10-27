# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

import sys

# Test Casses
from tests import auth_test
from tests import get_logger
from tests import api_config_test
from tests import test_mistral
from tests import test_gemini, test_gemini_agent
from tests import test_groq
from tests import (
    test_base_estimator_inheritance,
    test_base_estimator_methods,
    test_agent_classes_validation,
    test_ddgs_web_search,
    test_groq_endpoints,
    test_agent_endpoints,
)
from tests.gemini_agent_test import (
    case_tools_none,
    case_tools_empty_list,
    case_tools_wrong_type_string,
    case_tools_wrong_type_int,
    case_tools_wrong_type_dict,
    case_tools_missing_description,
    case_tools_missing_name,
    case_tools_empty_dict_in_list,
)
from dotenv import load_dotenv
load_dotenv()


logger = get_logger(__name__)


def auth_testing():
    # logger.info("Running auth test suite")
    print("=========== Running auth test suite ===========")

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
        print("=========== All Test Case Passed 4/4 ===========")
        return True

    logger.error("Test Case #4 Failed with correct master key.")
    return False

def api_config_testing():
    # logger.info("Running API config TestCases.")
    print("=========== Running API config TestCases ===========")

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

    print("=========== All Test Case Passed 7/7 ===========")
    return True
    
def mistral_testing():
    FAKE_KEY = "my_mistral_key"
    # logger.info("Running MistralAI TestCases with fake api.")
    print("=========== Running MistralAI TestCases with Fake API ===========")

    logger.info("TestCase #1 - KEY & query both None.")
    val, result = test_mistral()
    logger.debug(f"case #1 result - {result}")
    if not(val):
        logger.error(f"TestCase #1 Failed.")
        return False

    logger.info("TestCase #2 - query = None")
    val, result = test_mistral(KEY=FAKE_KEY)
    logger.debug(f"case #2 result - {result}")
    if not(val):
        logger.error("TestCase #2 Failed.")
        return False

    logger.info("TestCase #3 - valid value with real_api=False")
    val, result = test_mistral(KEY=FAKE_KEY, query="hey", real_api=False)
    logger.debug(f"case #3 result - {result}")
    if not(val):
        logger.error("TestCase #3 Failed.")
        return False

    logger.info("TestCase #4 - valid value with real_api=True with fake api")
    val, result = test_mistral(KEY=FAKE_KEY, query="hey", real_api=True)
    logger.debug(f"case #4 result - {result}")
    if val != False:
        logger.error("TestCase #4 Failed.")
        return False

    print("=========== All Test Case Passed 4/4 ===========")

    # Secret Test case only for prod testing with real_api key

    # val, result = test_mistral(KEY="actual_api_key", query="Hello!", real_api=True)
    # print(val, result)

    
    # if val:
    #     logger.info("testCase passed with real api key")
    #     return True
    # else:
    #     return False # Else API didn't worked or internel things crashed

    return True # End if no secret key test

def gemini_testing():
    FAKE_KEY = "my_gemini_key"
    print("=========== Running ChatGemini TestCases with Fake API ===========")

    logger.info("TestCase #1 - KEY & query both None.")
    val, result = test_gemini()
    logger.debug(f"case #1 result - {result}")
    if not(val):
        logger.error(f"TestCase #1 Failed.")
        return False

    logger.info("TestCase #2 - query = None")
    val, result = test_gemini(KEY=FAKE_KEY)
    logger.debug(f"case #2 result - {result}")
    if not(val):
        logger.error("TestCase #2 Failed.")
        return False

    logger.info("TestCase #3 - valid value with real_api=False")
    val, result = test_gemini(KEY=FAKE_KEY, query="hey", real_api=False)
    logger.debug(f"case #3 result - {result}")
    if not(val):
        logger.error("TestCase #3 Failed.")
        return False

    logger.info("TestCase #4 - valid value with real_api=True with fake api")
    val, result = test_gemini(KEY=FAKE_KEY, query="hey", real_api=True)
    logger.debug(f"case #4 result - {result}")
    if val != False:
        logger.error("TestCase #4 Failed.")
        return False

    print("=========== All Test Case Passed 4/4 ===========")

    # Secret Test case only for prod testing with real_api key

    # val, result = test_gemini(KEY="actual_api_key", query="Hello!", real_api=True)
    # print(val, result)

    
    # if val:
    #     logger.info("testCase passed with real api key")
    #     return True
    # else:
    #     return False # Else API didn't worked or internel things crashed

    return True # End if no secret key test

def groq_testing():
    FAKE_KEY = "my_groq_key"
    print("=========== Running ChatGroq TestCases with Fake API ===========")

    logger.info("TestCase #1 - KEY & query both None.")
    val, result = test_groq()
    logger.debug(f"case #1 result - {result}")
    if not(val):
        logger.error("TestCase #1 Failed.")
        return False

    logger.info("TestCase #2 - query = None")
    val, result = test_groq(KEY=FAKE_KEY)
    logger.debug(f"case #2 result - {result}")
    if not(val):
        logger.error("TestCase #2 Failed.")
        return False

    logger.info("TestCase #3 - valid value with real_api=True with fake api")
    val, result = test_groq(KEY=FAKE_KEY, query="hey", real_api=True)
    logger.debug(f"case #3 result - {result}")
    if val != False:
        logger.error("TestCase #3 Failed.")
        return False

    print("=========== All Test Case Passed 4/4 ===========")
    return True


def test_gemini_agent():
    print("=========== Running GeminiAgent tools_info TestCases ===========")

    cases = [
        ("TestCase #1 - tools_info=None",                 case_tools_none),
        ("TestCase #2 - tools_info=[] (empty list)",      case_tools_empty_list),
        ("TestCase #3 - tools_info='search' (string)",    case_tools_wrong_type_string),
        ("TestCase #4 - tools_info=42 (int)",             case_tools_wrong_type_int),
        ("TestCase #5 - tools_info={} (bare dict)",       case_tools_wrong_type_dict),
        ("TestCase #6 - missing 'description' key",       case_tools_missing_description),
        ("TestCase #7 - missing 'name' key",              case_tools_missing_name),
        ("TestCase #8 - [{}] empty dict in list",         case_tools_empty_dict_in_list),
    ]

    passed = 0
    for label, case_fn in cases:
        logger.info(label)
        val, result = case_fn()
        logger.debug(f"Result: {result}")
        if val:
            passed += 1
        else:
            logger.error(f"{label} — FAILED: {result}")
            return False

    print(f"=========== All Test Cases Passed {passed}/{len(cases)} ===========")
    return True


def base_estimator_testing():
    print("=========== Running BaseEstimator, Agent Classes & Endpoints TestCases ===========")
    cases = [
        ("TestCase #1 - BaseEstimator & BaseEstimatorAgent inheritance", test_base_estimator_inheritance),
        ("TestCase #2 - BaseEstimator validation & parameter methods", test_base_estimator_methods),
        ("TestCase #3 - Agent classes tools_info validation (Gemini, Groq, Mistral)", test_agent_classes_validation),
        ("TestCase #4 - DDGS web_search tool check", test_ddgs_web_search),
        ("TestCase #5 - Groq chat & parameters endpoints (/v1/groq/chat, /v1/groq/parameters)", test_groq_endpoints),
        ("TestCase #6 - Agent endpoints (/v1/gemini/agent, /v1/groq/agent, /v1/mistral/agent)", test_agent_endpoints),
    ]

    passed = 0
    for label, case_fn in cases:
        logger.info(label)
        val, result = case_fn()
        logger.debug(f"Result: {result}")
        if val:
            passed += 1
        else:
            logger.error(f"{label} — FAILED: {result}")
            return False

    print(f"=========== All Test Cases Passed {passed}/{len(cases)} ===========")
    return True


def main():
    results = []
    results.append(auth_testing())        # Auth Test Case
    results.append(api_config_testing())  # API config Test Case
    results.append(mistral_testing())     # Mistral provider testing
    results.append(gemini_testing())      # Gemini Testing
    results.append(groq_testing())        # Groq Testing
    results.append(test_gemini_agent())   # GeminiAgent tools_info Testing
    results.append(base_estimator_testing())  # BaseEstimator & Groq endpoints Testing

    return all(results) # Return False if any Test Case Failed
    


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
