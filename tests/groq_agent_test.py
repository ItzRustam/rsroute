# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for GroqAgent tools_info validation, parameters, and inheritance.
NOTE: These tests only cover tools_info input validation and parameter holding — no real API key required.
"""

from app.providers import GroqAgent
from app.providers.base import BaseAgentModel, BaseChatModel
from app.Errors import InvalidRequest

FAKE_KEY = "my_groq_fake_key"

def test_groq_agent(tools: list = None, api_key: str = FAKE_KEY):
    """Run GroqAgent with given tools_info and return (passed, message).

    Returns:
        (True,  message) — InvalidRequest was raised as expected (validation caught it).
        (False, message) — Unexpected exception or unexpected success.
    """
    try:
        agent = GroqAgent(api_key=api_key, tools_info=tools, max_retries=0)
    except InvalidRequest as IR:
        return True, str(IR)   # Expected — validation rejected bad input
    except Exception as E:
        return False, str(E)   # Unexpected crash
    else:
        return False, "Agent initialised without error — should have raised InvalidRequest"


# --- Individual named cases ---

def case_tools_none():
    """tools_info=None — should raise InvalidRequest."""
    return test_groq_agent(tools=None)

def case_tools_empty_list():
    """tools_info=[] — empty list, should raise InvalidRequest."""
    return test_groq_agent(tools=[])

def case_tools_wrong_type_string():
    """tools_info='search' — a string instead of list, should raise InvalidRequest."""
    return test_groq_agent(tools="search")

def case_tools_wrong_type_int():
    """tools_info=42 — an int instead of list, should raise InvalidRequest."""
    return test_groq_agent(tools=42)

def case_tools_wrong_type_dict():
    """tools_info={} — a bare dict instead of list, should raise InvalidRequest."""
    return test_groq_agent(tools={})

def case_tools_missing_description():
    """tools_info=[{"name": "search"}] — missing 'description' key."""
    return test_groq_agent(tools=[{"name": "search"}])

def case_tools_missing_name():
    """tools_info=[{"description": "search the web"}] — missing 'name' key."""
    return test_groq_agent(tools=[{"description": "search the web"}])

def case_tools_empty_dict_in_list():
    """tools_info=[{}] — dict with no keys at all."""
    return test_groq_agent(tools=[{}])

def case_api_key_none():
    """api_key=None — should raise InvalidRequest."""
    tool = [{"name": "web_search", "description": "Search the web"}]
    try:
        GroqAgent(api_key=None, tools_info=tool)
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
        agent = GroqAgent(
            api_key=FAKE_KEY,
            tools_info=tool,
            model="openai/gpt-oss-120b",
            temperature=0.5,
            max_tokens=1000,
            max_retries=0,
            end_point="https://api.groq.com/openai/v1",
        )
        params = agent.get_params()
        assert params.get("model") == "openai/gpt-oss-120b", "model parameter mismatch"
        assert params.get("temperature") == 0.5, "temperature parameter mismatch"
        assert params.get("max_tokens") == 1000, "max_tokens parameter mismatch"
        assert params.get("max_retries") == 0, "max_retries parameter mismatch"
        assert params.get("end_point") == "https://api.groq.com/openai/v1", "end_point parameter mismatch"
        assert params.get("binded_tools") == tool, "binded_tools parameter mismatch"
        return True, "Valid initialization and params check passed"
    except Exception as E:
        return False, str(E)

def case_agent_inheritance():
    """Verify GroqAgent inherits from BaseAgentModel and BaseChatModel."""
    try:
        assert issubclass(GroqAgent, BaseAgentModel), "Must inherit from BaseAgentModel"
        assert issubclass(GroqAgent, BaseChatModel), "Must inherit from BaseChatModel"
        return True, "GroqAgent inheritance check passed"
    except Exception as E:
        return False, str(E)

def case_agent_methods():
    """Verify GroqAgent implements generate, get_params, and __call__."""
    try:
        assert callable(getattr(GroqAgent, "generate", None)), "generate must be callable"
        assert callable(getattr(GroqAgent, "get_params", None)), "get_params must be callable"
        assert callable(getattr(GroqAgent, "__call__", None)), "__call__ must be callable"
        return True, "GroqAgent methods check passed"
    except Exception as E:
        return False, str(E)

