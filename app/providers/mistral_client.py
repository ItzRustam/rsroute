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
from typing import Any, Dict

"""
TODO
Add Embedding Model Support
"""

"""Class MistralAI Does not supports `Streaming` & model_kwrags. supports only text-to-text"""
class MistralAI:
    def __init__(
        self,
        api_key : str = None,
        model : str = "mistral-small-2603",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        random_seed : int = 42,
        top_p : int = 1.0,
        stop = None,

        # Base url
        end_point : str = None,
        timeout : int = 120,
        max_retries : int = 5,
        max_concurrent_requests : int = 64
    ):

        """Integration with MistralAI via Langchain.

        This class provides a wrapper around Langchain's `ChatMistralAI` to simplify
        interaction with MistralAI's model endpoints. It abstracts away the configuration
        of connection settings, model parameters, and query handling.

        Attributes:
            __model (ChatMistralAI): Instance of Langchain's `ChatMistralAI` configured with
                the specified parameters.
            __params (Dict[Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Raises:
            InvalidRequest: If `api_key` is not provided during initialization.

        Example:
            Initialize the MistralAI client with a specific model and API key:
            ```python
            llm = MistralAI(model="mistral-small", api_key="my_mistral_api_key")
            response = llm("What is Langchain?")
            ```

        Usage:
            - Create an instance of `MistralAI` with desired parameters.
            - Call the instance like a function to generate responses.
            - Utilize `get_params()` to retrieve the initialization parameters.

        Note:
            The class currently supports text-to-text generation and does not expose
            advanced streaming or additional model keyword arguments.
        """
        
        if api_key is None:
            raise InvalidRequest(f"API key is not given.")

        self.__model = ChatMistralAI(model_name=model, 
                                    temperature=temperature, 
                                    max_tokens=max_tokens, 
                                    random_seed=random_seed,
                                    top_p=top_p, 
                                    stop=stop,
                                    base_url=end_point,
                                    timeout=timeout,
                                    max_retries=max_retries,
                                    max_concurrent_requests=max_concurrent_requests,
                                    api_key=api_key)

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

    def generate(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            str: The generated response from MistralAI.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        if query is None:
            raise InvalidRequest(f"`query` is given `None`")
        
        return self.__model.invoke(input=query)

    def get_params(self):
        """Get the parameters used during initialization.

        Returns:
            Dict[Any]: A dictionary containing the initialization parameters.
        """
        return self.__params

    """Example:
        model = MistralAI(model="mistral-small", api_key="my_mistral_api_key")
        response = model("wtf")
    """
    def __call__(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            str: The generated response from MistralAI.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        return self.generate(query=query)


if __name__ == "__main__":
    llm = MistralAI(model="mistral-small", api_key="mistral_key_pls")
    response = llm(query="Hello? how are the Decoder Style Transformer Architecture are built?")