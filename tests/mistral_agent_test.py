# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for MistralAgent tools_info validation, parameters, and inheritance.
NOTE: These tests only cover tools_info input validation and parameter holding — no real API key required.
"""

from app.providers import MistralAgent
from app.providers.base import BaseAgentModel, BaseChatModel
from app.Errors import InvalidRequest

FAKE_KEY = "my_mistral_fake_key"

def test_mistral_agent(tools: list = None, api_key: str = FAKE_KEY):
    """Run MistralAgent with given tools_info and return (passed, message).

    Returns:
        (True,  message) — InvalidRequest was raised as expected (validation caught it).
        (False, message) — Unexpected exception or unexpected success.
    """
    try:
        agent = MistralAgent(api_key=api_key, tools_info=tools, max_retries=0)
    except InvalidRequest as IR:
        return True, str(IR)   # Expected — validation rejected bad input
    except Exception as E:
        return False, str(E)   # Unexpected crash
    else:
        return False, "Agent initialised without error — should have raised InvalidRequest"


# --- Individual named cases ---

def case_tools_none():
    """tools_info=None — should raise InvalidRequest."""
    return test_mistral_agent(tools=None)

def case_tools_empty_list():
    """tools_info=[] — empty list, should raise InvalidRequest."""
    return test_mistral_agent(tools=[])

def case_tools_wrong_type_string():
    """tools_info='search' — a string instead of list, should raise InvalidRequest."""
    return test_mistral_agent(tools="search")

def case_tools_wrong_type_int():
    """tools_info=42 — an int instead of list, should raise InvalidRequest."""
    return test_mistral_agent(tools=42)

def case_tools_wrong_type_dict():
    """tools_info={} — a bare dict instead of list, should raise InvalidRequest."""
    return test_mistral_agent(tools={})

def case_tools_missing_description():
    """tools_info=[{"name": "search"}] — missing 'description' key."""
    return test_mistral_agent(tools=[{"name": "search"}])

def case_tools_missing_name():
    """tools_info=[{"description": "search the web"}] — missing 'name' key."""
    return test_mistral_agent(tools=[{"description": "search the web"}])

def case_tools_empty_dict_in_list():
    """tools_info=[{}] — dict with no keys at all."""
    return test_mistral_agent(tools=[{}])

def case_api_key_none():
    """api_key=None — should raise InvalidRequest."""
    tool = [{"name": "web_search", "description": "Search the web"}]
    try:
        MistralAgent(api_key=None, tools_info=tool)
    except InvalidRequest:
        return True, "InvalidRequest raised as expected for api_key=None"
    except Exception as E:
        return False, str(E)
    else:
        return False, "Agent initialised without error when api_key=None"

def case_valid_initialization():
    """Valid api_key and tools_info — should initialize and hold all parameters."""
    tool = [{"name": "web_search", "description": "Search the web"}]
    try:
        agent = MistralAgent(
            api_key=FAKE_KEY,
            tools_info=tool,
            model="mistral-small-2603",
            temperature=0.5,
            max_tokens=1000,
            max_retries=0,
            top_p=0.9,
            end_point="https://api.mistral.ai",
        )
        params = agent.get_params()
        assert params.get("model") == "mistral-small-2603", "model parameter mismatch"
        assert params.get("temperature") == 0.5, "temperature parameter mismatch"
        assert params.get("max_tokens") == 1000, "max_tokens parameter mismatch"
        assert params.get("max_retries") == 0, "max_retries parameter mismatch"
        assert params.get("top_p") == 0.9, "top_p parameter mismatch"
        assert params.get("end_point") == "https://api.mistral.ai", "end_point parameter mismatch"
        assert params.get("binded_tools") == tool, "binded_tools parameter mismatch"
        return True, "Valid initialization and params check passed"
    except Exception as E:
        return False, str(E)

def case_agent_inheritance():
    """Verify MistralAgent inherits from BaseAgentModel and BaseChatModel."""
    try:
        assert issubclass(MistralAgent, BaseAgentModel), "Must inherit from BaseAgentModel"
        assert issubclass(MistralAgent, BaseChatModel), "Must inherit from BaseChatModel"
        return True, "MistralAgent inheritance check passed"
    except Exception as E:
        return False, str(E)

def case_agent_methods():
    """Verify MistralAgent implements generate, get_params, and __call__."""
    try:
        assert callable(getattr(MistralAgent, "generate", None)), "generate must be callable"
        assert callable(getattr(MistralAgent, "get_params", None)), "get_params must be callable"
        assert callable(getattr(MistralAgent, "__call__", None)), "__call__ must be callable"
        return True, "MistralAgent methods check passed"
    except Exception as E:
        return False, str(E)

