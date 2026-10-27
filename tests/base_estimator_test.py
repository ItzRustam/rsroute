# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for BaseEstimator and Groq server endpoints."""

from app.providers import BaseEstimator, ChatGroq, ChatGemini, ChatMistralAI, MistralAI
from app.Errors import InvalidRequest
from fastapi.testclient import TestClient
from app.server import create_server


def test_base_estimator_inheritance():
    """Verify all provider classes inherit from BaseEstimator."""
    assert issubclass(ChatGroq, BaseEstimator), "ChatGroq must be a subclass of BaseEstimator"
    assert issubclass(ChatGemini, BaseEstimator), "ChatGemini must be a subclass of BaseEstimator"
    assert issubclass(ChatMistralAI, BaseEstimator), "ChatMistralAI must be a subclass of BaseEstimator"
    assert issubclass(MistralAI, BaseEstimator), "MistralAI must be a subclass of BaseEstimator"
    assert ChatMistralAI is MistralAI, "ChatMistralAI should alias MistralAI"
    return True, "All provider classes inherit from BaseEstimator"


def test_base_estimator_methods():
    """Verify BaseEstimator parameter and query validation behavior."""
    # Test api_key=None raises InvalidRequest
    try:
        ChatGroq(api_key=None)
        return False, "ChatGroq should raise InvalidRequest when api_key=None"
    except InvalidRequest:
        pass

    try:
        ChatGemini(api_key=None)
        return False, "ChatGemini should raise InvalidRequest when api_key=None"
    except InvalidRequest:
        pass

    try:
        ChatMistralAI(api_key=None)
        return False, "ChatMistralAI should raise InvalidRequest when api_key=None"
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
    assert "tools_info" not in params_data, "'tools_info' must not be in Groq parameters info"
    assert "tools_info_example (not a parameter)" not in params_data, "tools_info_example must not be in Groq parameters"
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

