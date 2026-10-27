# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Helpful tools for server to improve code reusability"""

from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from langchain.messages import AIMessage

# NOTE: Do not use it directly, always make .copy() and then edit/send.
PARAMS_INFO : Dict[str, str] = {
    "query": "Input to Model",
    "master_key": "rsroute key, mandatory to send response, change it in `.env`",
    "model": "Model name",
    "temperature": "Model creativity scale from 0.0 to 1.0 default is 0.7. Mid-Creative",
    "max_token": "Maximum Tokens To generate in each request",
    "top_p": "Nucleus sampling token selection boundary (0.0 to 1.0)",
    "end_point": "Custom url to connect to model.",
    "tools_info" : "Bind Your Tool. (only in `/agent` mode)",

    "tools_info_example (not a parameter)": """[{"name": "tool_name", "description": "tool_description"}, {"name": "tool2_name", "description": "description of tool2"}]"""
}

class ResponseTemplate(BaseModel):
    """FastAPI server response Template."""
    content : Any
    query : List[Any]
    error : str
    login : bool
    auth: bool
    # Optional when .invoke() never trigers
    usage_metadata : Optional[dict] = None
    response_metadata : Optional[dict] = None

    # Optional when model never initlized.
    initlized_parameters : Optional[dict] = None

class AgentTemplate(BaseModel):
    """FastAPI server response Template For Agent."""
    content : Any
    tool_calls : Optional[List[Dict[Any, Any]]] = []
    query : List[Any]
    error : str
    login : bool
    auth: bool
    # Optional when .invoke() never trigers
    usage_metadata : Optional[dict] = None
    response_metadata : Optional[dict] = None

    # Optional when model never initlized.
    initlized_parameters : Optional[dict] = None


def convertAgentResponse(response : AIMessage, 
    query : List[Any], 
    error : str, 
    auth : bool, 
    login : bool, 
    initlized_params : dict
) -> dict:
    """RSRoute tool to convert Model AIMessage to FastAPI result according to AgentTemplate"""
    # Metadata & content
    content = response.content
    usage_metadata : dict = response.usage_metadata
    response_metadata : dict = response.response_metadata

    tool_calls = response.tool_calls

    # Pydantic Instance
    result = AgentTemplate(content=content,
                              tool_calls=tool_calls,
                              query=query,
                              error=error,
                              login=login,
                              auth=auth,
                              usage_metadata=usage_metadata,
                              response_metadata=response_metadata,
                              initlized_parameters=initlized_params)

    # returning Dict
    return result.model_dump()


def convertResponse(response : AIMessage, 
    query : str, 
    error : str, 
    auth : bool, 
    login : bool, 
    initlized_params : dict
) -> dict:
    """RSRoute tool to convert Model AIMessage to FastAPI result according to ResponseTemplate"""
    # Metadata & content
    content = response.content
    usage_metadata : dict = response.usage_metadata
    response_metadata : dict = response.response_metadata

    # Pydantic Instance
    result = ResponseTemplate(content=content,
                              query=query,
                              error=error,
                              login=login,
                              auth=auth,
                              usage_metadata=usage_metadata,
                              response_metadata=response_metadata,
                              initlized_parameters=initlized_params)

    # returning Dict
    return result.model_dump()
    
    
