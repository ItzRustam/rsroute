# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for BaseChatModel, BaseAgentModel, and agent server endpoints."""

from app.providers import (
    BaseChatModel,
    BaseAgentModel,
    ChatGroq,
    ChatGemini,
    ChatMistralAI,
    MistralAI,
    ChatOpenRouter,
    GeminiAgent,
    GroqAgent,
    MistralAgent,
    OpenRouterAgent,
    ChatOpenAI,
    OpenAIAgent,
    ChatOpenAIAgent,
)
from app.Errors import InvalidRequest
from fastapi.testclient import TestClient
from app.server import create_server
from test_server import web_search, WEB_SEARCH_TOOL


def test_base_estimator_inheritance():
    """Verify all provider classes inherit from BaseChatModel and BaseAgentModel."""
    # BaseChatModel inheritance
    assert issubclass(ChatGroq, BaseChatModel), "ChatGroq must be a subclass of BaseChatModel"
    assert issubclass(ChatGemini, BaseChatModel), "ChatGemini must be a subclass of BaseChatModel"
    assert issubclass(ChatMistralAI, BaseChatModel), "ChatMistralAI must be a subclass of BaseChatModel"
    assert issubclass(MistralAI, BaseChatModel), "MistralAI must be a subclass of BaseChatModel"
    assert issubclass(ChatOpenRouter, BaseChatModel), "ChatOpenRouter must be a subclass of BaseChatModel"
    assert issubclass(ChatOpenAI, BaseChatModel), "ChatOpenAI must be a subclass of BaseChatModel"
    assert ChatMistralAI is MistralAI, "ChatMistralAI should alias MistralAI"

    # BaseAgentModel inheritance
    assert issubclass(BaseAgentModel, BaseChatModel), "BaseAgentModel must be a subclass of BaseChatModel"
    assert issubclass(GeminiAgent, BaseAgentModel), "GeminiAgent must be a subclass of BaseAgentModel"
    assert issubclass(GroqAgent, BaseAgentModel), "GroqAgent must be a subclass of BaseAgentModel"
    assert issubclass(MistralAgent, BaseAgentModel), "MistralAgent must be a subclass of BaseAgentModel"
    assert issubclass(OpenRouterAgent, BaseAgentModel), "OpenRouterAgent must be a subclass of BaseAgentModel"
    assert issubclass(OpenAIAgent, BaseAgentModel), "OpenAIAgent must be a subclass of BaseAgentModel"
    assert OpenAIAgent is ChatOpenAIAgent, "OpenAIAgent should alias ChatOpenAIAgent"

    return True, "All provider and agent classes inherit from BaseChatModel / BaseAgentModel"


def test_base_estimator_methods():
    """Verify BaseChatModel parameter and query validation behavior."""
    # Test api_key=None raises InvalidRequest
    for cls in [ChatGroq, ChatGemini, ChatMistralAI, ChatOpenRouter, ChatOpenAI]:
        try:
            cls(api_key=None)
            return False, f"{cls.__name__} should raise InvalidRequest when api_key=None"
        except InvalidRequest:
            pass

    # Test get_params on initialized instance
    groq = ChatGroq(api_key="fake_groq_key", max_retries=0)
    params = groq.get_params()
    assert "model" in params, "params must contain 'model'"
    assert "max_tokens" in params, "params must contain 'max_tokens'"

    openai_client = ChatOpenAI(api_key="fake_openai_key", max_retries=0)
    openai_params = openai_client.get_params()
    assert "model" in openai_params, "openai_params must contain 'model'"
    assert "timeout" in openai_params, "openai_params must contain 'timeout'"

    return True, "BaseChatModel methods and validation passed"


def test_agent_classes_validation():
    """Verify tools_info validation across all agent classes."""
    tool = {"name": "web_search", "description": "Search the web"}

    # Test api_key=None
    for agent_cls in [GeminiAgent, GroqAgent, MistralAgent, OpenRouterAgent, OpenAIAgent]:
        try:
            agent_cls(api_key=None, tools_info=[tool], max_retries=0)
            return False, f"{agent_cls.__name__} should raise InvalidRequest when api_key=None"
        except InvalidRequest:
            pass

        # Test tools_info=None
        try:
            agent_cls(api_key="fake_key", tools_info=None, max_retries=0)
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tools_info=None"
        except InvalidRequest:
            pass

        # Test tools_info=[]
        try:
            agent_cls(api_key="fake_key", tools_info=[], max_retries=0)
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tools_info=[]"
        except InvalidRequest:
            pass

        # Test tools_info missing description
        try:
            agent_cls(api_key="fake_key", tools_info=[{"name": "search"}], max_retries=0)
            return False, f"{agent_cls.__name__} should raise InvalidRequest when tool missing description"
        except InvalidRequest:
            pass

        # Test valid initialization
        agent = agent_cls(api_key="fake_key", tools_info=[tool], max_retries=0)
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
    res_chat_bad_auth = client.post("/v1/groq/chat", json={"query": "Hello", "master_key": "bad_key", "max_retries": 0})
    assert res_chat_bad_auth.status_code == 200
    assert res_chat_bad_auth.json().get("login") is False

    # Test chat endpoint with valid master key but without GROQ_API_KEY
    res_chat_valid_auth = client.post("/v1/groq/chat", json={"query": "Hello", "master_key": "RSRoute_my_key", "max_retries": 0})
    assert res_chat_valid_auth.status_code == 200
    assert "login" in res_chat_valid_auth.json()

    return True, "Groq endpoints /v1/groq/chat & /v1/groq/parameters passed"


def test_openrouter_endpoints():
    """Verify /v1/openrouter/chat and /v1/openrouter/parameters endpoints."""
    server = create_server()
    client = TestClient(server)

    # Plural and singular parameters endpoints
    res_params = client.get("/v1/openrouter/parameters")
    assert res_params.status_code == 200, f"Expected 200, got {res_params.status_code}"
    params_data = res_params.json()

    res_param = client.get("/v1/openrouter/parameter")
    assert res_param.status_code == 200, f"Expected 200, got {res_param.status_code}"

    # Verify parameters info adheres to requirements
    assert "top_p" not in params_data, "'top_p' must not be in OpenRouter parameters info"
    assert "max_tokens" in params_data, "'max_tokens' must be in OpenRouter parameters info"
    assert "query" in params_data, "'query' must be in OpenRouter parameters info"
    assert "master_key" in params_data, "'master_key' must be in OpenRouter parameters info"
    assert "model" in params_data, "'model' must be in OpenRouter parameters info"
    assert "temperature" in params_data, "'temperature' must be in OpenRouter parameters info"
    assert "app_title" in params_data, "'app_title' must be in OpenRouter parameters info"
    assert "app_url" in params_data, "'app_url' must be in OpenRouter parameters info"
    assert "providers" in params_data, "'providers' must be in OpenRouter parameters info"

    # Test chat endpoint with invalid master key (when auth enabled)
    res_chat_bad_auth = client.post("/v1/openrouter/chat", json={"query": "Hello", "master_key": "bad_key", "max_retries": 0})
    assert res_chat_bad_auth.status_code == 200
    assert res_chat_bad_auth.json().get("login") is False

    # Test chat endpoint with valid master key
    res_chat_valid_auth = client.post("/v1/openrouter/chat", json={"query": "Hello", "master_key": "RSRoute_my_key", "max_retries": 0})
    assert res_chat_valid_auth.status_code == 200
    assert "login" in res_chat_valid_auth.json()

    return True, "OpenRouter endpoints /v1/openrouter/chat & /v1/openrouter/parameters passed"


def test_openai_endpoints():
    """Verify /v1/openai/chat, /v1/openai/agent, and /v1/openai/parameters endpoints."""
    import os
    server = create_server()
    client = TestClient(server)

    # Plural and singular parameters endpoints
    res_params = client.get("/v1/openai/parameters")
    assert res_params.status_code == 200, f"Expected 200, got {res_params.status_code}"
    params_data = res_params.json()

    res_param = client.get("/v1/openai/parameter")
    assert res_param.status_code == 200, f"Expected 200, got {res_param.status_code}"

    # Verify parameters info adheres to requirements
    assert "top_p" not in params_data, "'top_p' must not be in OpenAI parameters info"
    assert "max_tokens" in params_data, "'max_tokens' must be in OpenAI parameters info"
    assert "query" in params_data, "'query' must be in OpenAI parameters info"
    assert "master_key" in params_data, "'master_key' must be in OpenAI parameters info"
    assert "model" in params_data, "'model' must be in OpenAI parameters info"
    assert "temperature" in params_data, "'temperature' must be in OpenAI parameters info"
    assert "timeout" in params_data, "'timeout' must be in OpenAI parameters info"
    assert "use_response_api" in params_data, "'use_response_api' must be in OpenAI parameters info"
    assert "organization_id" in params_data, "'organization_id' must be in OpenAI parameters info"

    # Test chat endpoint with invalid master key (when auth enabled)
    res_chat_bad_auth = client.post("/v1/openai/chat", json={"query": "Hello", "master_key": "bad_key", "max_retries": 0})
    assert res_chat_bad_auth.status_code == 200
    assert res_chat_bad_auth.json().get("login") is False

    # Test chat endpoint with valid master key but without OPENAI_API_KEY
    orig_key = os.environ.get("OPENAI_API_KEY")
    orig_org = os.environ.get("OPENAI_ORG_ID")
    try:
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("OPENAI_ORG_ID", None)

        res_chat_no_key = client.post("/v1/openai/chat", json={"query": "Hello", "master_key": "RSRoute_my_key", "max_retries": 0})
        assert res_chat_no_key.status_code == 200
        assert res_chat_no_key.json().get("login") is True
        assert "No OpenAI API Key Found" in res_chat_no_key.json().get("error", "")

        # With OPENAI_API_KEY set, but no organization_id provided or in env
        os.environ["OPENAI_API_KEY"] = "sk-fake-key"
        res_chat_no_org = client.post("/v1/openai/chat", json={"query": "Hello", "master_key": "RSRoute_my_key", "max_retries": 0})
        assert res_chat_no_org.status_code == 200
        assert "No OpenAI Organization ID Found" in res_chat_no_org.json().get("error", "")

        # Test agent endpoint with invalid master key
        res_agent_bad_auth = client.post("/v1/openai/agent", json={
            "query": "Hello",
            "master_key": "bad_key",
            "tools_info": [WEB_SEARCH_TOOL],
            "max_retries": 0,
        })
        assert res_agent_bad_auth.status_code == 200
        assert res_agent_bad_auth.json().get("login") is False
        assert "tool_calls" in res_agent_bad_auth.json()

        # Test agent endpoint with valid key but no org id
        res_agent_no_org = client.post("/v1/openai/agent", json={
            "query": "Hello",
            "master_key": "RSRoute_my_key",
            "tools_info": [WEB_SEARCH_TOOL],
            "max_retries": 0,
        })
        assert res_agent_no_org.status_code == 200
        assert "No OpenAI Organization ID Found" in res_agent_no_org.json().get("error", "")
        assert "tool_calls" in res_agent_no_org.json()
    finally:
        if orig_key is not None:
            os.environ["OPENAI_API_KEY"] = orig_key
        else:
            os.environ.pop("OPENAI_API_KEY", None)
        if orig_org is not None:
            os.environ["OPENAI_ORG_ID"] = orig_org
        else:
            os.environ.pop("OPENAI_ORG_ID", None)

    return True, "OpenAI endpoints /v1/openai/chat, /v1/openai/agent & /v1/openai/parameters passed"


def test_agent_endpoints():
    """Verify /v1/gemini/agent, /v1/groq/agent, /v1/mistral/agent, /v1/openrouter/agent, and /v1/openai/agent endpoints."""
    server = create_server()
    client = TestClient(server)

    endpoints = [
        "/v1/gemini/agent",
        "/v1/groq/agent",
        "/v1/mistral/agent",
        "/v1/openrouter/agent",
        "/v1/openai/agent",
    ]

    for ep in endpoints:
        # Invalid auth
        res_bad = client.post(ep, json={
            "query": "Hello",
            "master_key": "invalid_key",
            "tools_info": [WEB_SEARCH_TOOL],
            "max_retries": 0,
        })
        assert res_bad.status_code == 200, f"{ep} expected 200, got {res_bad.status_code}"
        assert res_bad.json().get("login") is False, f"{ep} login should be False with invalid key"
        assert "tool_calls" in res_bad.json(), f"{ep} must return tool_calls field in AgentTemplate"

        # Valid master key
        res_valid = client.post(ep, json={
            "query": "Hello",
            "master_key": "RSRoute_my_key",
            "tools_info": [WEB_SEARCH_TOOL],
            "max_retries": 0,
        })
        assert res_valid.status_code == 200, f"{ep} expected 200, got {res_valid.status_code}"
        assert "login" in res_valid.json(), f"{ep} must return login status"
        assert "tool_calls" in res_valid.json(), f"{ep} must return tool_calls field"

    return True, "All agent endpoints (/v1/gemini/agent, /v1/groq/agent, /v1/mistral/agent, /v1/openrouter/agent, /v1/openai/agent) passed"

