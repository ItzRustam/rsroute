# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: separate Mistral Route from other routes."""

"""TODO: /embed end point for embedding models"""

from app.providers import MistralAI, MistralAgent
from fastapi import APIRouter, Body
from app.Errors import *
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import os
from app.auth import auth_exits, auth
from app.server.tools import (
    ResponseTemplate,
    convertResponse,
    AgentTemplate,
    convertAgentResponse,
    PARAMS_INFO,
)

load_dotenv()  # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits()  # True, False


router = APIRouter(
    prefix="/v1/mistral",
    tags=["MistralAI", "Agent", "ChatModel"]
)

@router.get("/parameters")
@router.get("/parameter")
def parameters() -> dict:
    params = PARAMS_INFO.copy()
    return params


@router.post("/chat")
def chat(
         query: Any = Body("Hello"),
         master_key: str = Body(""),
         model: str = Body("mistral-small-2603"),
         temperature: float = Body(0.7),
         max_tokens: int = Body(2048),
         top_p: float = Body(1.0),
         # Base url
         end_point: Optional[str] = Body(None),
         ):
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
            response = ResponseTemplate(content="Authentication Failed", error=ERROR, login=LOGIN, query=query,
                                        auth=AUTH_ENABLE)
            return response.model_dump()

    else:
        pass
        # pass your Time without a password to your APIs

    if os.getenv("MISTRAL_API_KEY"):
        pass  # Key Passed
    else:
        response = ResponseTemplate(content="Invalid Request", error="No MistralAI API Key Found, try to edit `.env`",
                                    login=LOGIN, query=query, auth=AUTH_ENABLE)
        return response.model_dump()

    model_instance: MistralAI = MistralAI(api_key=os.getenv("MISTRAL_API_KEY"),
                                          model=model,
                                          temperature=temperature,
                                          max_tokens=max_tokens,
                                          top_p=top_p,
                                          end_point=end_point,
                                          )

    try:
        result = model_instance(query)  # getting result
    except Exception as E:
        response = ResponseTemplate(content="Request Error", error=str(E),
                                    login=LOGIN, query=query, auth=AUTH_ENABLE)

        return response.model_dump()
    else:
        # output for request
        return convertResponse(response=result, query=query, error=ERROR, auth=AUTH_ENABLE, login=LOGIN,
                               initlized_params=model_instance.get_params())


@router.post("/agent")
def agent(
    query: Any = Body("Hello"),
    master_key: str = Body(""),
    model: str = Body("mistral-small-2603"),
    temperature: float = Body(0.7),
    max_tokens: int = Body(2048),
    top_p: float = Body(1.0),
    end_point: Optional[str] = Body(None),
    tools_info: List[Dict[str, str]] = Body(None)
):
    """Agent endpoint for Mistral models with tool binding."""
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

    if os.getenv("MISTRAL_API_KEY"):
        pass  # Key Passed
    else:
        response = AgentTemplate(
            content="Invalid Request",
            error="No MistralAI API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    try:
        model_instance: MistralAgent = MistralAgent(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            end_point=end_point,
            tools_info=tools_info
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




