# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: saprate Gemini Route from Other's route."""
"""TODO: /embed end point for embedding models"""

from app.providers import ChatGemini
from fastapi import APIRouter
from app.Errors import *
from dotenv import load_dotenv
import os
from app.auth import auth_exits, auth
from app.server.tools import ResponseTemplate, convertResponse

load_dotenv() # Loading Environment

# AUTH ENABLE or DISABLE
AUTH_ENABLE = auth_exits() # True, False



"""TESTING CODE"""
router = APIRouter(
    prefix="/v1/gemini",
    tags=["Gemini", "Google"]
)

@router.post("/chat")
def chat(query : str = "Hello", 
        master_key : str = "", 
        model : str = "gemini-3.5-flash-lite", 
        temperature : float = 0.7,
        max_tokens : int = 2048,

        top_p : int = 1.0,
        
        # Base url
        end_point : str = None,
        thinking_level : str = None,
        thinking_budget : int = None
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
            response = ResponseTemplate(content="Authentication Failed", error=ERROR, login=LOGIN, query=query, auth=AUTH_ENABLE)
            return response.model_dump()

    else:
        pass
        # pass your Time without a password to your APIs

    if os.getenv("GOOGLE_API_KEY"):
        pass # Key Passed
    else:
        response = ResponseTemplate(content="GInvalid Request", error="No Google API Key Found, try to edit `.env`", login=LOGIN, query=query, auth=AUTH_ENABLE)
        return response.model_dump()
    

    model : ChatGemini = ChatGemini(api_key=os.getenv("GOOGLE_API_KEY"),
                       model=model,
                       temperature=temperature,
                       max_tokens=max_tokens,
                       top_p=top_p,
                       end_point=end_point,
                       thinking_budget=thinking_budget,
                       thinking_level=thinking_level)

    result = model(query) # getting result

    # output for request
    return convertResponse(response=result, query=query, error=ERROR, auth=AUTH_ENABLE, login=LOGIN, initlized_params=model.get_params())

