# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from .mistral_client import MistralAI
from .gemini_client import ChatGemini

__all__ = ["MistralAI", "ChatGemini"]

"""Parameters for Each Function Call
model_name
provider_name
prompt : anything langchain supports
maximum_output_token
specific
"""