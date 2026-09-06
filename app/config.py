# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional
import os
from app.Errors import *

# v1 Providers
_OPEN_AI_API_KEY = "OPENAI_API_KEY"
_MISTRALAI_KEY = "MISTRAL_API_KEY"
_HF_TOKEN = "HUGGINGFACEHUB_API_TOKEN"
_OPENROUTER_KEY = "OPENROUTER_API_KEY"
_GEMINI_KEY = "GOOGLE_API_KEY"
_GROQ_API_KEY = "GROQ_API_KEY"
SUPPORTED_PROVIDERS = [_OPEN_AI_API_KEY, _OPENROUTER_KEY, _HF_TOKEN, _MISTRALAI_KEY, _GEMINI_KEY, _GROQ_API_KEY]

# Config Idea Credit
# https://github.com/fnnx-ai/scikit-llm
# Config File :- https://github.com/fnnx-ai/scikit-llm/blob/main/skllm/config.py

# When To use

# Use full when Library mood
# changing `.env` is recommended
# Useful only when changing to quick new API key.
# DO NOT USE THIS CLASS ON PROD FASTAPI SERVER
class RSRouteConfig:
    @staticmethod
    def set_openai_key(key : str) -> None:
        """
        Sets the OpenAI key.  

        Parameters  
        ----------  
        key : str, Can't be None
            OpenAI Key.

        """
        os.environ[_OPEN_AI_API_KEY] = key

    @staticmethod
    def set_gemini_key(key : str) -> None:
            """
            Sets the Gemini key.  
    
            Parameters  
            ----------  
            key : str, Can't be None
                Gemini Key.
    
            """
            os.environ[_GEMINI_KEY] = key

    @staticmethod
    def set_mistral_key(key : str) -> None:
            """
            Sets the MistralAI key.  
    
            Parameters  
            ----------  
            key : str, Can't be None
                MistralAI Key.
    
            """
            os.environ[_MISTRALAI_KEY] = key

    @staticmethod
    def set_hf_key(key : str) -> None:
            """
            Sets the Huggingface key.  
    
            Parameters  
            ----------  
            key : str, Can't be None
                Huggingface Key.
    
            """
            os.environ[_HF_TOKEN] = key

    @staticmethod
    def set_openrouter_key(key : str) -> None:
            """
            Sets the OpenRouter key.  
    
            Parameters  
            ----------  
            key : str, Can't be None
                OpenRouter Key.
    
            """
            os.environ[_OPENROUTER_KEY] = key

    @staticmethod
    def set_groq_key(key : str) -> None:
            """
            Sets the Groq key.  
    
            Parameters  
            ----------  
            key : str, Can't be None
                Groq Key.
    
            """  
            os.environ[_GROQ_API_KEY] = key


def is_api(api_keyword : str):
    """Function to Test if API exits on .env or not."""

    # Unsupported Provider
    if api_keyword not in SUPPORTED_PROVIDERS:
        raise UnsupportedProvider(f"{api_keyword} is not supported, only {SUPPORTED_PROVIDERS} are supported")

    # If api does not exits
    if not os.getenv(api_keyword):
        return False

    # else api exits
    return True