# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: separate OpenAI Route from other routes."""

from app.providers import ChatOpenAI, OpenAIAgent
from app.defaults import OPENAI_DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE, TIMEOUT, MAX_RETRIES, QUERY
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
    get_org_id,
)
from typing import Dict, Any, List, Optional

load_dotenv()  # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits()  # True, False

router = APIRouter(
    prefix="/v1/openai",
    tags=["OpenAI", "Agent", "ChatModel"]
)


@router.get("/parameters")
@router.get("/parameter")
def parameters() -> dict:
    """Return supported parameter information for OpenAI."""
    params = PARAMS_INFO.copy()
    params.pop("top_p", None)
    params["model"] = f"Model name, default is {OPENAI_DEFAULT_MODEL}"
    params["max_tokens"] = f"Maximum tokens to generate in each request, default is {MAX_TOKENS}"
    params["temperature"] = f"Creativity/randomness control (0.0 to 2.0), default is {TEMPERATURE}"
    params["timeout"] = f"Network request timeout in seconds, default is {TIMEOUT}"
    params["max_retries"] = f"Maximum automated retry attempts on request failure, default is {MAX_RETRIES}"
    params["use_response_api"] = "Whether to use the OpenAI Responses API instead of Chat Completions (default: False)"
    params["organization_id"] = "OpenAI organization identifier, default picked from .env"
    return params


@router.post("/chat")
def chat(
    query: Any = Body(QUERY),
    master_key: str = Body(""),
    model: str = Body(OPENAI_DEFAULT_MODEL),
    temperature: float = Body(TEMPERATURE),
    max_tokens: int = Body(MAX_TOKENS),
    max_retries: int = Body(MAX_RETRIES),
    timeout: int = Body(TIMEOUT),
    use_response_api: bool = Body(False),
    end_point: Optional[str] = Body(None),
    organization_id: Optional[str] = Body(None),
):
    """Chat endpoint for OpenAI models."""
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

    if os.getenv("OPENAI_API_KEY"):
        pass  # Key Passed
    else:
        response = ResponseTemplate(
            content="Invalid Request",
            error="No OpenAI API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()


    if organization_id is None:
        organization_id = get_org_id()

    if not organization_id:
        response = ResponseTemplate(
            content="Invalid Request",
            error="No OpenAI Organization ID Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        model_instance: ChatOpenAI = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            timeout=timeout,
            use_response_api=use_response_api,
            end_point=end_point,
            organization_id=organization_id,
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
    query: Any = Body(QUERY),
    master_key: str = Body(""),
    model: str = Body(OPENAI_DEFAULT_MODEL),
    temperature: float = Body(TEMPERATURE),
    max_tokens: int = Body(MAX_TOKENS),
    max_retries: int = Body(MAX_RETRIES),
    timeout: int = Body(TIMEOUT),
    use_response_api: bool = Body(False),
    end_point: Optional[str] = Body(None),
    organization_id: Optional[str] = Body(None),
    tools_info: Optional[List[Dict[str, str]]] = Body(None),
):
    """Agent endpoint for OpenAI models with tool binding."""
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

    if os.getenv("OPENAI_API_KEY"):
        pass  # Key Passed
    else:
        response = AgentTemplate(
            content="Invalid Request",
            error="No OpenAI API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()


    if organization_id is None:
        organization_id = get_org_id()

    if not organization_id:
        response = AgentTemplate(
            content="Invalid Request",
            error="No OpenAI Organization ID Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        model_instance: OpenAIAgent = OpenAIAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            timeout=timeout,
            use_response_api=use_response_api,
            end_point=end_point,
            organization_id=organization_id,
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
