# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: separate OpenRouter Route from other routes."""

from app.providers import ChatOpenRouter, OpenRouterAgent
from app.defaults import DEFAULT_OPENROUTER_MODEL, MAX_TOKENS, TEMPERATURE
from fastapi import APIRouter, Body
from app.Errors import *
from dotenv import load_dotenv
import os
from app.auth import auth_exits, auth
from app.server.tools import (
    ResponseTemplate,
    convertResponse,
    AgentTemplate,
    convertAgentResponse,
    PARAMS_INFO,
)
from typing import Dict, Any, List, Optional

load_dotenv()  # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits()  # True, False

router = APIRouter(
    prefix="/v1/openrouter",
    tags=["OpenRouter", "Agent", "ChatModel"]
)


@router.get("/parameters")
@router.get("/parameter")
def parameters() -> dict:
    """Return supported parameter information for OpenRouter."""
    params = PARAMS_INFO.copy()
    params.pop("top_p", None)
    params["model"] = f"Model name, default is {DEFAULT_OPENROUTER_MODEL}"
    params["max_tokens"] = f"Maximum tokens to generate in each request, default is {MAX_TOKENS}"
    params["temperature"] = f"Sampling temperature from 0.0 to 2.0, default is {TEMPERATURE}"
    params["app_title"] = "Application title for OpenRouter rankings (default: 'RSRoute')"
    params["app_url"] = "Application URL for OpenRouter rankings (default: 'https://www.rsroute.freedev.app/')"
    params["app_categories"] = "List of category strings for OpenRouter rankings"
    params["max_retries"] = "Maximum automated retry attempts on request failure (default: 2)"
    params["providers"] = "OpenRouter provider preferences dictionary (e.g. {'order': ['OpenAI']})"
    return params


@router.post("/chat")
def chat(
    query: Any = Body("Hello"),
    master_key: str = Body(""),
    model: str = Body(DEFAULT_OPENROUTER_MODEL),
    temperature: float = Body(TEMPERATURE),
    max_tokens: int = Body(MAX_TOKENS),
    app_title: str = Body("RSRoute"),
    app_url: str = Body("https://www.rsroute.freedev.app/"),
    app_categories: Optional[List[str]] = Body(None),
    max_retries: int = Body(2),
    providers: Optional[Dict[Any, Any]] = Body(None),
    end_point: Optional[str] = Body(None),
):
    """Chat endpoint for OpenRouter models."""
    if not isinstance(query, list):
        query = [query]

    # Base Initialization
    LOGIN = False
    ERROR = "No Error Found"
    if AUTH_ENABLE:
        try:
            LOGIN = auth(master_key=master_key)
        except Exception as E:
            LOGIN = False
            ERROR = str(E)
            # Return Auth Error
            response = ResponseTemplate(
                content="Authentication Failed",
                error=ERROR,
                login=LOGIN,
                query=query,
                auth=AUTH_ENABLE
            )
            return response.model_dump()
    else:
        pass

    if os.getenv("OPENROUTER_API_KEY"):
        pass  # Key Passed
    else:
        response = ResponseTemplate(
            content="Invalid Request",
            error="No OpenRouter API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        model_instance: ChatOpenRouter = ChatOpenRouter(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            app_title=app_title,
            app_url=app_url,
            app_categories=app_categories,
            max_retries=max_retries,
            providers=providers,
            end_point=end_point,
        )
    except Exception as E:
        response = ResponseTemplate(
            content="Invalid Request",
            error=str(E),
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        result = model_instance(query)  # getting result
    except Exception as E:
        response = ResponseTemplate(
            content="Request Error",
            error=str(E),
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()
    else:
        # output for request
        return convertResponse(
            response=result,
            query=query,
            error=ERROR,
            auth=AUTH_ENABLE,
            login=LOGIN,
            initlized_params=model_instance.get_params()
        )


@router.post("/agent")
def agent(
    query: Any = Body("Hello"),
    master_key: str = Body(""),
    model: str = Body(DEFAULT_OPENROUTER_MODEL),
    temperature: float = Body(TEMPERATURE),
    max_tokens: int = Body(MAX_TOKENS),
    app_title: str = Body("RSRoute"),
    app_url: str = Body("https://www.rsroute.freedev.app/"),
    app_categories: Optional[List[str]] = Body(None),
    max_retries: int = Body(2),
    providers: Optional[Dict[Any, Any]] = Body(None),
    end_point: Optional[str] = Body(None),
    tools_info: Optional[List[Dict[str, str]]] = Body(None),
):
    """Agent endpoint for OpenRouter models with tool binding."""
    if not isinstance(query, list):
        query = [query]

    # Base Initialization
    LOGIN = False
    ERROR = "No Error Found"
    if AUTH_ENABLE:
        try:
            LOGIN = auth(master_key=master_key)
        except Exception as E:
            LOGIN = False
            ERROR = str(E)
            # Return Auth Error
            response = AgentTemplate(
                content="Authentication Failed",
                error=ERROR,
                login=LOGIN,
                query=query,
                auth=AUTH_ENABLE
            )
            return response.model_dump()
    else:
        pass

    if os.getenv("OPENROUTER_API_KEY"):
        pass  # Key Passed
    else:
        response = AgentTemplate(
            content="Invalid Request",
            error="No OpenRouter API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        model_instance: OpenRouterAgent = OpenRouterAgent(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            app_title=app_title,
            app_url=app_url,
            app_categories=app_categories,
            max_retries=max_retries,
            providers=providers,
            end_point=end_point,
            tools_info=tools_info,
        )
    except Exception as E:
        response = AgentTemplate(
            content="Invalid Request",
            error=str(E),
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        result = model_instance(query)  # getting result
    except Exception as E:
        response = AgentTemplate(
            content="Request Error",
            error=str(E),
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()
    else:
        # output for request
        return convertAgentResponse(
            response=result,
            query=query,
            error=ERROR,
            auth=AUTH_ENABLE,
            login=LOGIN,
            initlized_params=model_instance.get_params()
        )

