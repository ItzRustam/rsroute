# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Helpful tools for server to improve code reusability"""

from pydantic import BaseModel
from typing import Optional, Any
from langchain.messages import AIMessage


class ResponseTemplate(BaseModel):
    """FastAPI server response Template."""
    content : Any
    query : str
    error : str
    login : bool
    auth: bool
    # Optional when .invoke() never trigers
    usage_metadata : Optional[dict] = None
    response_metadata : Optional[dict] = None

    # Optional when model never initlized.
    initlized_parameters : Optional[dict] = None


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
    
    