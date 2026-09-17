# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Purpose: saprate Gemini Route from Other's route."""

from app.providers import ChatGemini
from fastapi import APIRouter


"""TESTING CODE"""
router = APIRouter(
    prefix="/v1/gemini",
    tags=["Gemini", "Google"]
)

@router.post("/chat")
def chat(query : str = "wth?"):
    return {"content": "why? why? really..."}

