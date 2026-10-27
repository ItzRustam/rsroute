# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""server route connector for diffrent diffrent provider"""
# NOTE: server doesn't support Tool Binding/calling
from .root import router as root_router
from .gemini_route import router as g_route # gemini_route
from .mistral_route import router as m_route # mistral_route
from .groq_route import router as groq_route # groq_route
from fastapi import FastAPI


def create_server() -> FastAPI:
    """
    RSRoute
    -------
    Create FastAPI server on Initialized router.
    
    Available routers
    ----------------
    Gemini: route to chat with Gemini  
        route: /v1/gemini/chat
    MistralAI: route to chat with Mistral AI
        route: /v1/mistral/chat
    Groq: route to chat with Groq
        route: /v1/groq/chat

    Returns
    -------
    * FastAPI
    """    

    server = FastAPI(
        title="RSRoute"
    )

    server.include_router(root_router) # Root Route
    server.include_router(g_route) # Gemini Router Added
    server.include_router(m_route) # MistralAI Router Added
    server.include_router(groq_route) # Groq Router Added

    return server # return FastAPI server.
