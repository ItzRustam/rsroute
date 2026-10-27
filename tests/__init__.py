# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from .auth_tests import auth_test
from .logger import get_logger
from .api_config_test import api_config_test
from .mistral_client_test import test_mistral
from .gemini_client_test import test_gemini
from .groq_client_test import test_groq
from .gemini_agent_test import test_gemini_agent
from .base_estimator_test import (
    test_base_estimator_inheritance,
    test_base_estimator_methods,
    test_agent_classes_validation,
    test_ddgs_web_search,
    test_groq_endpoints,
    test_agent_endpoints,
)

# Added logger for colorful logging in test cases
__all__ = [
    "auth_test",
    "get_logger",
    "api_config_test",
    "test_mistral",
    "test_gemini",
    "test_groq",
    "test_gemini_agent",
    "test_base_estimator_inheritance",
    "test_base_estimator_methods",
    "test_agent_classes_validation",
    "test_ddgs_web_search",
    "test_groq_endpoints",
    "test_agent_endpoints",
]
