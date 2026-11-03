# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from .base import BaseChatModel, BaseAgentModel
from .mistral_client import MistralAI, ChatMistralAI, MistralAgent, ChatMistralAgent
from .gemini_client import ChatGemini, GeminiAgent
from .groq_client import ChatGroq, GroqAgent
from .openrouter_client import ChatOpenRouter, OpenRouterAgent, ChatOpenRouterAgent

__all__ = [
    "BaseChatModel",
    "BaseAgentModel",
    "MistralAI",
    "ChatMistralAI",
    "MistralAgent",
    "ChatMistralAgent",
    "ChatGemini",
    "GeminiAgent",
    "ChatGroq",
    "GroqAgent",
    "ChatOpenRouter",
    "OpenRouterAgent",
    "ChatOpenRouterAgent"
]

"""Parameters for Each Function Call
model_name
provider_name
prompt : anything langchain supports
maximum_output_token
specific
"""
