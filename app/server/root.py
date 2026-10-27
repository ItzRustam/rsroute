# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""/ (root) starting point for FastAPI server"""
"""It will include end-point details"""

from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["v1", "root", "home"]
)

@router.get("/")
def root():
    return {
        "content": {
            "title": "RSRoute Home Page",
            "description": "Home Page for FastAPI Server",
            "routes": {
                "Google Gemini": {
                    "description": "Connect to Google Gemini with agentic powers.",
                    "ChatModel": "/v1/gemini/chat",
                    "Agent": "/v1/gemini/agent",
                    "EmbeddingModel": "Coming Soon",
                    "ParameterInfo": "/v1/gemini/parameter",
                    "support tools": True,
                },
                "MistralAI": {
                    "description": "Connect to MistralAI with agentic powers.",
                    "ChatModel": "/v1/mistral/chat",
                    "Agent": "/v1/mistral/agent",
                    "ParameterInfo": "/v1/mistral/parameter",
                    "EmbeddingModel": "Coming Soon",
                    "support tools": True,
                },
                "Groq": {
                    "description": "Connect to Groq with agentic powers.",
                    "ChatModel": "/v1/groq/chat",
                    "Agent": "/v1/groq/agent",
                    "ParameterInfo": "/v1/groq/parameters",
                    "EmbeddingModel": "Coming Soon",
                    "support tools": True,
                },
            },
            "NOTE": "use exact `master_key` given in `.env` or else it won't work. don't forget to put API key which model you wanna use.",
            "GitHub": "https://www.github.com/ItzRustam/rsroute",
            "By": "ItzRustam (Rustam Bhadouriya)",
            "version": "v1-starter-version",
        }
    }
