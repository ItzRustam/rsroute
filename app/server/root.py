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
                    "ChatModel": "/v1/gemini/chat",
                    "EmbeddingModel": "Coming Soon",
                    "ParameterInfo": "/v1/gemini/parameter",
                    "support tools": False,
                },
                "MistralAI": {
                    "ChatModel": "/v1/mistral/chat",
                    "ParameterInfo": "/v1/mistral/parameter",
                    "EmbeddingModel": "Coming Soon",
                    "support tools": False,
                },

            },
            "NOTE": "use exact `master_key` given in `.env` or else it won't work. don't forget to put API key which model you wanna use.",
            "GitHub": "https://www.github.com/ItzRustam/rsroute",
            "By": "ItzRustam (Rustam Bhadouriya)",
            "version": "v1-starter-version",
        }
    }