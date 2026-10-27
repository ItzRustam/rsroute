# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from .base import BaseEstimator, BaseEstimatorAgent
from .mistral_client import MistralAI, ChatMistralAI, MistralAgent, ChatMistralAgent
from .gemini_client import ChatGemini, GeminiAgent
from .groq_client import ChatGroq, GroqAgent

__all__ = [
    "BaseEstimator",
    "BaseEstimatorAgent",
    "MistralAI",
    "ChatMistralAI",
    "MistralAgent",
    "ChatMistralAgent",
    "ChatGemini",
    "GeminiAgent",
    "ChatGroq",
    "GroqAgent",
]

"""Parameters for Each Function Call
model_name
provider_name
prompt : anything langchain supports
maximum_output_token
specific
"""
