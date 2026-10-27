# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from .base import BaseEstimator
from .mistral_client import MistralAI, ChatMistralAI
from .gemini_client import ChatGemini, GeminiAgent
from .groq_client import ChatGroq

__all__ = ["BaseEstimator", "MistralAI", "ChatMistralAI", "ChatGemini", "ChatGroq", "GeminiAgent"]

"""Parameters for Each Function Call
model_name
provider_name
prompt : anything langchain supports
maximum_output_token
specific
"""
