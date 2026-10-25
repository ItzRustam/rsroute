# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for GeminiAgent tools_info validation.
NOTE: These tests only cover tools_info input validation — no real API key required.
"""

from app.providers import GeminiAgent
from app.Errors import InvalidRequest

FAKE_KEY = "my_gemini_fake_key"

def test_gemini_agent(tools: list, api_key: str = FAKE_KEY):
    """Run GeminiAgent with given tools_info and return (passed, message).

    Returns:
        (True,  message) — InvalidRequest was raised as expected (validation caught it).
        (False, message) — Unexpected exception or unexpected success.
    """
    try:
        agent = GeminiAgent(api_key=api_key, tools_info=tools)
    except InvalidRequest as IR:
        return True, str(IR)   # Expected — validation rejected bad input
    except Exception as E:
        return False, str(E)   # Unexpected crash
    else:
        return False, "Agent initialised without error — should have raised InvalidRequest"


# --- Individual named cases ---

def case_tools_none():
    """tools_info=None — should raise InvalidRequest."""
    return test_gemini_agent(tools=None)

def case_tools_empty_list():
    """tools_info=[] — empty list, should raise InvalidRequest."""
    return test_gemini_agent(tools=[])

def case_tools_wrong_type_string():
    """tools_info='search' — a string instead of list, should raise InvalidRequest."""
    return test_gemini_agent(tools="search")

def case_tools_wrong_type_int():
    """tools_info=42 — an int instead of list, should raise InvalidRequest."""
    return test_gemini_agent(tools=42)

def case_tools_wrong_type_dict():
    """tools_info={} — a bare dict instead of list, should raise InvalidRequest."""
    return test_gemini_agent(tools={})

def case_tools_missing_description():
    """tools_info=[{"name": "search"}] — missing 'description' key."""
    return test_gemini_agent(tools=[{"name": "search"}])

def case_tools_missing_name():
    """tools_info=[{"description": "search the web"}] — missing 'name' key."""
    return test_gemini_agent(tools=[{"description": "search the web"}])

def case_tools_empty_dict_in_list():
    """tools_info=[{}] — dict with no keys at all."""
    return test_gemini_agent(tools=[{}])