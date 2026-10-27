# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""This File Contains rsroute integration with MistralAI using Langchain."""

"""Langchain-mistral ChatMistralAI parameters

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

"""     
        INFO
Parameter removed
* random_seed
* stop
* max_concurrent_requests
* max_retries
* timeout

"""

from langchain_mistralai import ChatMistralAI as _LangchainChatMistralAI
from app.Errors import *
from typing import Any, Dict, List, Optional
import warnings
from app.providers.base import BaseEstimator, BaseEstimatorAgent

"""
TODO
Add Embedding Model Support
"""

"""Class ChatMistralAI Does not supports `Streaming` & model_kwargs. supports only text-to-text"""
class ChatMistralAI(BaseEstimator):
    def __init__(
        self,
        api_key : str = None,
        model : str = "mistral-small-2603",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        top_p : float = 1.0,

        # Base url
        end_point : str = None,
    ):

        """Integration with MistralAI via Langchain.

        This class provides a wrapper around Langchain's `ChatMistralAI` to simplify
        interaction with MistralAI's model endpoints. It abstracts away the configuration
        of connection settings, model parameters, and query handling.

        Attributes:
            _model (_LangchainChatMistralAI): Instance of Langchain's `ChatMistralAI` configured with
                the specified parameters.
            _params (Dict[Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Raises:
            InvalidRequest: If `api_key` is not provided during initialization.

        Example:
            Initialize the MistralAI client with a specific model and API key:
            ```python
            llm = ChatMistralAI(model="mistral-small", api_key="my_mistral_api_key")
            response = llm("What is Langchain?")
            ```

        Usage:
            - Create an instance of `ChatMistralAI` with desired parameters.
            - Call the instance like a function to generate responses.
            - Utilize `get_params()` to retrieve the initialization parameters.

        Note:
            The class currently supports text-to-text generation and does not expose
            advanced streaming or additional model keyword arguments.
        """
        super().__init__()
        self._validate_api_key(api_key)

        self._model = _LangchainChatMistralAI(model_name=model,
                                             temperature=temperature,
                                             max_tokens=max_tokens,
                                             top_p=top_p,
                                             base_url=end_point,
                                             api_key=api_key)

        # Saving model initialize parameters
        self._params : Dict[Any, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "top_p" : top_p,
            "end_point" : end_point, # base_url,
        }

        # Backwards compatibility attributes
        self.__model = self._model
        self.__params = self._params

    def generate(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            str: The generated response from MistralAI.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        return super().generate(query=query)

    def get_params(self):
        """Get the parameters used during initialization.

        Returns:
            Dict[Any]: A dictionary containing the initialization parameters.
        """
        return super().get_params()

    """Example:
        model = ChatMistralAI(model="mistral-small", api_key="my_mistral_api_key")
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


# Backward compatibility alias so nothing breaks
MistralAI = ChatMistralAI


class MistralAgent(BaseEstimatorAgent):
    def __init__(
        self,
        api_key : str = None,
        model : str = "mistral-small-2603",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        top_p : float = 1.0,

        # Base url
        end_point : str = None,

        tools_info : List[Dict[str, str]] = None
    ):
        """MistralAI-powered agentic wrapper with tool-binding support via Langchain.

        Wraps `ChatMistralAI` and binds fake/stub tools to the model,
        enabling the model to reason about and invoke external tools by name.

        Args:
            api_key (str): Mistral API credential key. Required.
            model (str): Target Mistral model name. Defaults to ``"mistral-small-2603"``.
            temperature (float): Creativity/randomness control (0.0–2.0). Defaults to ``0.7``.
            max_tokens (int): Maximum tokens to generate per response. Defaults to ``2048``.
            top_p (float): Nucleus sampling threshold (0.0–1.0). Defaults to ``1.0``.
            end_point (str): Custom base URL for proxy servers or API gateways. Optional.
            tools_info (List[Dict[str, str]]): List of tool definitions to bind to the agent.
                Each entry must have ``"name"`` and ``"description"`` keys. Required.

        Raises:
            InvalidRequest: If ``api_key`` is ``None``.
            InvalidRequest: If ``tools_info`` is ``None``, empty, not a list, or contains non-dict entries.
        """
        warnings.warn("For Best Agentic Experience use rsroute python package. https://www.github.com/ItzRustam/rsroute-package")
        super().__init__()
        self._validate_api_key(api_key)
        self._validate_tools_info(tools_info)

        created_tools = self._create_fake_tools(tools_info=tools_info)

        self._params : Dict[str, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "top_p" : top_p,
            "end_point" : end_point,
            "binded_tools": tools_info,
        }

        self._model = _LangchainChatMistralAI(
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            base_url=end_point,
            api_key=api_key
        ).bind_tools(tools=created_tools)

        self.__agent = self._model
        self.__params = self._params

    def generate(self, query : Any = None):
        """Generate response on given `query`."""
        return super().generate(query=query)

    def get_params(self):
        """Model initialized parameters."""
        return super().get_params()

    def __call__(self, query : Any = None):
        """Generate response on given `query`. Same as `generate()`."""
        return self.generate(query=query)


ChatMistralAgent = MistralAgent


if __name__ == "__main__":
    llm = ChatMistralAI(model="mistral-small", api_key="mistral_key_pls")
    response = llm(query="Hello? how are the Decoder Style Transformer Architecture are built?")
