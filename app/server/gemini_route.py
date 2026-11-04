# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: saprate Gemini Route from Other's route."""
"""TODO: /embed end point for embedding models"""

from app.providers import ChatGemini, GeminiAgent
from fastapi import APIRouter, Body
from app.Errors import *
from dotenv import load_dotenv
import os
from app.auth import auth_exits, auth
from app.server.tools import ResponseTemplate, convertResponse, AgentTemplate, convertAgentResponse
from app.server.tools import PARAMS_INFO
from pydantic import BaseModel, Field

from app.defaults import DEFAULT_GEMINI_MODEL, MAX_RETRIES, MAX_TOKENS, TEMPERATURE, QUERY

from typing import Dict, Any, List, Optional

load_dotenv() # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits() # True, False




router = APIRouter(
    prefix="/v1/gemini",
    tags=["Gemini", "Google", "Agent", "ChatModel"]
)

@router.get("/parameters")
@router.get("/parameter")
def parameters() -> dict:
    params = PARAMS_INFO.copy()
    params["thinking_budget"] = " configure the token limits for reasoning and chain-of-thought processing in supported Google Gemini models"
    params["thinking_level"] = " parameter allows you to control the depth of reasoning tokens that Gemini 3+ models generate before producing a final answer."
    return params

@router.post("/chat")
def chat(
        query : Any = Body(QUERY),
        master_key : str = Body(""),
        model : str = Body(DEFAULT_GEMINI_MODEL),
        temperature : float = Body(TEMPERATURE),
        max_tokens : int = Body(MAX_TOKENS),
        top_p : float = Body(1.0),
        max_retries: float = Body(MAX_RETRIES),
        # Base url
        end_point : str = Body(None),
        thinking_level : str = Body(None),
        thinking_budget : int = Body(None)
        ):

    if not isinstance(query, list):
        query = [query]

        
    
    # Base Initlization
    LOGIN = False
    ERROR = "No Error Found"
    if AUTH_ENABLE:
        try:
            LOGIN = auth(master_key=master_key)
        except Exception as E:
            LOGIN = False
            ERROR = str(E)
            # Return Auth Error
            response = ResponseTemplate(content="Authentication Failed", error=ERROR, login=LOGIN, query=query, auth=AUTH_ENABLE)
            return response.model_dump()

    else:
        pass
        # pass your Time without a password to your APIs

    if os.getenv("GOOGLE_API_KEY"):
        pass # Key Passed
    else:
        response = ResponseTemplate(content="Invalid Request", error="No Google API Key Found, try to edit `.env`", login=LOGIN, query=query, auth=AUTH_ENABLE)
        return response.model_dump()
    

    model : ChatGemini = ChatGemini(api_key=os.getenv("GOOGLE_API_KEY"),
                       model=model,
                       temperature=temperature,
                       max_tokens=max_tokens,
                       max_retries=max_retries,
                       top_p=top_p,
                       end_point=end_point,
                       thinking_budget=thinking_budget,
                       thinking_level=thinking_level)

    try:
        result = model(query)  # getting result
    except Exception as E:
        response = ResponseTemplate(content="Request Error", error=str(E),
                                    login=LOGIN, query=query, auth=AUTH_ENABLE)

        return response.model_dump()
    else:
        # output for request
        return convertResponse(response=result, query=query, error=ERROR, auth=AUTH_ENABLE, login=LOGIN,
                               initlized_params=model.get_params())



@router.post("/agent")
def agent(
    query: Any = Body(QUERY),
    master_key: str = Body(""), 
    model: str = Body(DEFAULT_GEMINI_MODEL), 
    temperature: float = Body(TEMPERATURE),
    max_tokens: int = Body(MAX_TOKENS),
    max_retries : int = Body(MAX_RETRIES),
    top_p: float = Body(1.0),
    end_point: str = Body(None),
    thinking_level: str = Body(None),
    thinking_budget: int = Body(None),
    tools_info: List[Dict[str, str]] = Body(None) # Forces it to read from JSON body
):
    
    # Base Initlization
    LOGIN = False
    ERROR = "No Error Found"
    if AUTH_ENABLE:
        try:
            LOGIN = auth(master_key=master_key)
        except Exception as E:
            LOGIN = False
            ERROR = str(E)
            # Return Auth Error
            response = AgentTemplate(content="Authentication Failed", error=ERROR, login=LOGIN, query=query, auth=AUTH_ENABLE)
            return response.model_dump()

    else:
        pass
        # pass your Time without a password to your APIs

    if os.getenv("GOOGLE_API_KEY"):
        pass # Key Passed
    else:
        response = AgentTemplate(content="Invalid Request", error="No Google API Key Found, try to edit `.env`", login=LOGIN, query=query, auth=AUTH_ENABLE)
        return response.model_dump()
    

    try:
        model : GeminiAgent = GeminiAgent(api_key=os.getenv("GOOGLE_API_KEY"),
                           model=model,
                           temperature=temperature,
                           max_tokens=max_tokens,
                           max_retries=max_retries,
                           top_p=top_p,
                           end_point=end_point,
                           thinking_budget=thinking_budget,
                           thinking_level=thinking_level,
                           tools_info=tools_info)
    except Exception as E:
        response = AgentTemplate(content="Invalid Request", error=str(E),
                                 login=LOGIN, query=query, auth=AUTH_ENABLE)
        return response.model_dump()

    try:
        result = model(query)  # getting result
    except Exception as E:
        response = AgentTemplate(content="Request Error", error=str(E),
                                    login=LOGIN, query=query, auth=AUTH_ENABLE)

        return response.model_dump()
    else:
        # output for request
        return convertAgentResponse(response=result, query=query, error=ERROR, auth=AUTH_ENABLE, login=LOGIN,
                               initlized_params=model.get_params())



