# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for BaseEstimator, BaseEstimatorAgent, and agent server endpoints."""

from app.providers import (
    BaseEstimator,
    BaseEstimatorAgent,
    ChatGroq,
    ChatGemini,
    ChatMistralAI,
    MistralAI,
    GeminiAgent,
    GroqAgent,
    MistralAgent,
)
from app.Errors import InvalidRequest
from fastapi.testclient import TestClient
from app.server import create_server
from test_server import web_search, WEB_SEARCH_TOOL


def test_base_estimator_inheritance():
    """Verify all provider classes inherit from BaseEstimator and BaseEstimatorAgent."""
    # BaseEstimator inheritance
    assert issubclass(ChatGroq, BaseEstimator), "ChatGroq must be a subclass of BaseEstimator"
    assert issubclass(ChatGemini, BaseEstimator), "ChatGemini must be a subclass of BaseEstimator"
    assert issubclass(ChatMistralAI, BaseEstimator), "ChatMistralAI must be a subclass of BaseEstimator"
    assert issubclass(MistralAI, BaseEstimator), "MistralAI must be a subclass of BaseEstimator"
    assert ChatMistralAI is MistralAI, "ChatMistralAI should alias MistralAI"

    # BaseEstimatorAgent inheritance
    assert issubclass(BaseEstimatorAgent, BaseEstimator), "BaseEstimatorAgent must be a subclass of BaseEstimator"
    assert issubclass(GeminiAgent, BaseEstimatorAgent), "GeminiAgent must be a subclass of BaseEstimatorAgent"
    assert issubclass(GroqAgent, BaseEstimatorAgent), "GroqAgent must be a subclass of BaseEstimatorAgent"
    assert issubclass(MistralAgent, BaseEstimatorAgent), "MistralAgent must be a subclass of BaseEstimatorAgent"

    return True, "All provider and agent classes inherit from BaseEstimator / BaseEstimatorAgent"


def test_base_estimator_methods():
    """Verify BaseEstimator parameter and query validation behavior."""
    # Test api_key=None raises InvalidRequest
    for cls in [ChatGroq, ChatGemini, ChatMistralAI]:
        try:
            cls(api_key=None)
            return False, f"{cls.__name__} should raise InvalidRequest when api_key=None"
        except InvalidRequest:
            pass

    # Test get_params and set_params on initialized instance
    groq = ChatGroq(api_key="fake_groq_key")
    params = groq.get_params()
    assert "model" in params, "params must contain 'model'"
    assert "max_tokens" in params, "params must contain 'max_tokens'"

    groq.set_params(custom_param="test")
    assert groq.get_params().get("custom_param") == "test", "set_params must update params"

    return True, "BaseEstimator methods and validation passed"


def test_agent_classes_validation():
    """Verify tools_info validation across all agent classes."""
    tool = {"name": "web_search", "description": "Search the web"}

    # Test api_key=None
    for agent_cls in [GeminiAgent, GroqAgent, MistralAgent]:
        try:
            agent_cls(api_key=None, tools_info=[tool])
            return False, f"{agent_cls.__name__} should raise InvalidRequest when api_key=None"
        except InvalidRequest:
            pass

        # Test tools_info=None
        try:
            agent_cls(api_key="fake_key", tools_info=None)
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tools_info=None"
        except InvalidRequest:
            pass

        # Test tools_info=[]
        try:
            agent_cls(api_key="fake_key", tools_info=[])
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tools_info=[]"
        except InvalidRequest:
            pass

        # Test tools_info missing description
        try:
            agent_cls(api_key="fake_key", tools_info=[{"name": "search"}])
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tool missing description"
        except InvalidRequest:
            pass

        # Test valid initialization
        agent = agent_cls(api_key="fake_key", tools_info=[tool])
        assert "binded_tools" in agent.get_params(), f"{agent_cls.__name__} get_params must contain binded_tools"

    return True, "All agent classes tools_info validation passed"


def test_ddgs_web_search():
    """Verify DDGS web_search tool function."""
    assert callable(web_search), "web_search must be callable"
    results = web_search("python programming", max_results=2)
    assert isinstance(results, list), "web_search must return a list"
    return True, "DDGS web_search tool verification passed"


def test_groq_endpoints():
    """Verify /v1/groq/chat and /v1/groq/parameters endpoints."""
    server = create_server()
    client = TestClient(server)

    # Plural and singular parameters endpoints
    res_params = client.get("/v1/groq/parameters")
    assert res_params.status_code == 200, f"Expected 200, got {res_params.status_code}"
    params_data = res_params.json()

    res_param = client.get("/v1/groq/parameter")
    assert res_param.status_code == 200, f"Expected 200, got {res_param.status_code}"

    # Verify parameters info adheres to requirements
    assert "top_p" not in params_data, "'top_p' must not be in Groq parameters info"
    assert "max_tokens" in params_data, "'max_tokens' must be in Groq parameters info"
    assert "query" in params_data, "'query' must be in Groq parameters info"
    assert "master_key" in params_data, "'master_key' must be in Groq parameters info"
    assert "model" in params_data, "'model' must be in Groq parameters info"
    assert "temperature" in params_data, "'temperature' must be in Groq parameters info"
    assert "end_point" in params_data, "'end_point' must be in Groq parameters info"

    # Test chat endpoint with invalid master key (when auth enabled)
    res_chat_bad_auth = client.post("/v1/groq/chat", json={"query": "Hello", "master_key": "bad_key"})
    assert res_chat_bad_auth.status_code == 200
    assert res_chat_bad_auth.json().get("login") is False

    # Test chat endpoint with valid master key but without GROQ_API_KEY
    res_chat_valid_auth = client.post("/v1/groq/chat", json={"query": "Hello", "master_key": "RSRoute_my_key"})
    assert res_chat_valid_auth.status_code == 200
    assert "login" in res_chat_valid_auth.json()

    return True, "Groq endpoints /v1/groq/chat & /v1/groq/parameters passed"


def test_agent_endpoints():
    """Verify /v1/gemini/agent, /v1/groq/agent, and /v1/mistral/agent endpoints."""
    server = create_server()
    client = TestClient(server)

    endpoints = ["/v1/gemini/agent", "/v1/groq/agent", "/v1/mistral/agent"]

    for ep in endpoints:
        # Invalid auth
        res_bad = client.post(ep, json={
            "query": "Hello",
            "master_key": "invalid_key",
            "tools_info": [WEB_SEARCH_TOOL]
        })
        assert res_bad.status_code == 200, f"{ep} expected 200, got {res_bad.status_code}"
        assert res_bad.json().get("login") is False, f"{ep} login should be False with invalid key"
        assert "tool_calls" in res_bad.json(), f"{ep} must return tool_calls field in AgentTemplate"

        # Valid master key
        res_valid = client.post(ep, json={
            "query": "Hello",
            "master_key": "RSRoute_my_key",
            "tools_info": [WEB_SEARCH_TOOL]
        })
        assert res_valid.status_code == 200, f"{ep} expected 200, got {res_valid.status_code}"
        assert "login" in res_valid.json(), f"{ep} must return login status"
        assert "tool_calls" in res_valid.json(), f"{ep} must return tool_calls field"

    return True, "All agent endpoints (/v1/gemini/agent, /v1/groq/agent, /v1/mistral/agent) passed"

def test_agent_endpoints():
    """Verify /v1/gemini/agent, /v1/groq/agent, and /v1/mistral/agent endpoints."""
    server = create_server()
    client = TestClient(server)

    endpoints = ["/v1/gemini/agent", "/v1/groq/agent", "/v1/mistral/agent"]

    for ep in endpoints:
        # Invalid auth
        res_bad = client.post(ep, json={
            "query": "Hello",
            "master_key": "invalid_key",
            "tools_info": [WEB_SEARCH_TOOL]
        })
        assert res_bad.status_code == 200, f"{ep} expected 200, got {res_bad.status_code}"
        assert res_bad.json().get("login") is False, f"{ep} login should be False with invalid key"
        assert "tool_calls" in res_bad.json(), f"{ep} must return tool_calls field in AgentTemplate"

        # Valid master key
        res_valid = client.post(ep, json={
            "query": "Hello",
            "master_key": "RSRoute_my_key",
            "tools_info": [WEB_SEARCH_TOOL]
        })
        assert res_valid.status_code == 200, f"{ep} expected 200, got {res_valid.status_code}"
        assert "login" in res_valid.json(), f"{ep} must return login status"
        assert "tool_calls" in res_valid.json(), f"{ep} must return tool_calls field"

    return True, "All agent endpoints (/v1/gemini/agent, /v1/groq/agent, /v1/mistral/agent) passed"

