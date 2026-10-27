# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: separate Groq Route from other routes."""

from app.providers import ChatGroq
from app.providers.groq_client import DEFAULT_GROQ_MODEL
from fastapi import APIRouter, Body
from app.Errors import *
from dotenv import load_dotenv
import os
from app.auth import auth_exits, auth
from app.server.tools import ResponseTemplate, convertResponse, PARAMS_INFO
from typing import Any, List, Optional

load_dotenv()  # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits()  # True, False

router = APIRouter(
    prefix="/v1/groq",
    tags=["Groq", "ChatModel"]
)


@router.get("/parameters")
def parameters() -> dict:
    """Return supported parameter information for Groq ChatModel."""
    params = PARAMS_INFO.copy()

    # Remove parameters that ChatGroq does not support
    params.pop("top_p", None)
    params.pop("tools_info", None)
    params.pop("tools_info_example (not a parameter)", None)

    # Change/ensure max_tokens is formatted according to ChatGroq
    if "max_token" in params:
        params["max_tokens"] = params.pop("max_token")

    # Update model parameter description for Groq default
    params["model"] = f"Model name, default is {DEFAULT_GROQ_MODEL}"

    return params


@router.post("/chat")
def chat(
    query: Any = Body("Hello"),
    master_key: str = Body(""),
    model: str = Body(DEFAULT_GROQ_MODEL),
    temperature: float = Body(0.7),
    max_tokens: int = Body(2048),
    end_point: Optional[str] = Body(None),
):
    """Chat endpoint for Groq models."""
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

    if os.getenv("GROQ_API_KEY"):
        pass  # Key Passed
    else:
        response = ResponseTemplate(
            content="Invalid Request",
            error="No Groq API Key Found, try to edit `.env`",
            login=LOGIN,
            query=query,
            auth=AUTH_ENABLE
        )
        return response.model_dump()

    model_instance: ChatGroq = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        end_point=end_point,
    )

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

