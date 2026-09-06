# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""This File Contains rsroute integration with MistralAI using Langchain."""

"""Langchain-mistal ChatMistralAI parameters

mistral_model = ChatMistralAI(
    # Core Client & Network Settings
    # mistral_api_key="your_api_key",       # Optional: Overrides MISTRAL_API_KEY environment variable
    endpoint="https://mistral.ai",   # Target API URL (change for custom proxies/VPCs)
    timeout=120,                            # Network request timeout in seconds
    max_retries=5,                          # Automated exponential back-off retries on failure
    max_concurrent_requests=64,             # Concurrency cap for async batch operations (.abatch)

    # Core Generation Framework
    model="mistral-large-latest",           # Model selection string
    temperature=0.7,                        # Sampling randomness (0.0 to 2.0)
    max_tokens=1024,                        # Cap on outbound token counts (None for max headroom)
    top_p=0.9,                              # Nucleus sampling token selection boundary (0.0 to 1.0)
    random_seed=42,                         # Fixes the engine's seed for deterministic responses
    stop=["[END]", "### Exit"],             # Up to 4 custom string sequences that halt generation
    
    # Safety & Features
    safe_mode=False,                        # Deprecated in modern API tiers, defaults to False
    safe_prompt=False,                      # Toggles Mistral's system-level content safety guardrails
    streaming=True,                         # Configures the class to natively handle real-time chunk streaming

    # Advanced Pass-through Dictionary
    model_kwargs={
        # Map any raw downstream API arguments here if introduced in future API updates
    }
)

"""

from langchain_mistralai import ChatMistralAI
from app.Errors import *
from dotenv import load_dotenv
from typing import Any, Dict

"""Class MistralAI Does not supports `Streaming` & model_kwrags. supports only text-to-text"""
class MistralAI:
    def __init__(
        self,
        api_key : str = None,
        model : str = "mistral-small-2603",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        random_seed : int = 67,
        top_p : int = 1.0,
        stop = None,

        # Base url
        end_point : str = None,
        timeout : int = 120,
        max_retries : int = 5,
        max_concurrent_requests : int = 64
    ):
        if api_key is None:
            raise InvalidRequest(f"API key is not given.")

        self.Model = ChatMistralAI(model_name=model, temperature=temperature, max_tokens=max_tokens, random_seed=random_seed,
                            top_p=top_p, stop=stop, base_url=end_point, timeout=timeout, max_retries=max_retries, max_concurrent_requests=max_concurrent_requests, api_key=api_key)

        # Saving model initlize parameters
        self.__params : Dict[Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "random_seed" : random_seed,
            "top_p" : top_p,
            "stop" : stop,
            "end_point" : end_point, # base_url,
            "timeout" : timeout,
            "max_retries" : max_retries,
            "max_concurrent_requests" : max_concurrent_requests
        }

    def generate(self, prompt : Any = None):
        "invoke function for MistralAI class"
        if prompt == None:
            raise InvalidRequest(f"`prompt` is given `None`")
        
        return self.Model.invoke(prompt)

    def get_params(self):
        "get params on class initlize"
        return self.__params
