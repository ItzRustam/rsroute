# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""server route connector for diffrent diffrent provider"""
from .gemini_route import router as g_route # gemini_route

from fastapi import FastAPI

def create_server() -> FastAPI:
    """
    RSRoute
    -------
    Create FastAPI server on Initlized router.
    
    Available routers
    ----------------
    Gemini: route to chat with Gemini  
        route: /v1/gemini/chat

    Returns
    -------
    * FastAPI
    """    

    server = FastAPI(
        title="RSRoute"
    )

    server.include_router(g_route) # Gemini Router Added

    return server # return FastAPI server.
