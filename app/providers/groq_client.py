# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""This File Contains rsroute integration with Groq using Langchain."""

"""
INFO
Parameters intentionally NOT exposed (removed on purpose)
* custom_get_token_ids
* model_kwargs
* timeout
* reasoning_format

Exposed: model, temperature, max_tokens, api_key, base_url (as `end_point`).
`max_retries` is not exposed either (same as MistralAI / ChatGemini), langchain default is used.
"""

from langchain_groq import ChatGroq as _LangchainChatGroq
from app.Errors import *
from typing import Any, Dict, Tuple

# Only these Groq models are allowed, nothing else.
# NOTE: `qwen/qwen3.8-27b` is a *preview* model on Groq (not for production use).
GROQ_MODELS: Tuple[str, ...] = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
)
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"

"""Class ChatGroq Does not supports `Streaming` & model_kwargs. supports only text-to-text"""
class ChatGroq:
    def __init__(
        self,
        api_key : str = None,
        model : str = DEFAULT_GROQ_MODEL,
        temperature : float = 0.7,
        max_tokens : int = 2048,

        # Base url
        end_point : str = None,
    ):
        """Integration with Groq via Langchain.

        This class provides a wrapper around Langchain's `ChatGroq` to simplify
        interaction with Groq's model endpoints.

        Attributes:
            __model (ChatGroq): Instance of Langchain's `ChatGroq` configured with
                the specified parameters.
            __params (Dict[str, Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Raises:
            InvalidRequest: If `api_key` is not provided, or `model` is not in `GROQ_MODELS`.

        Example:
            ```python
            llm = ChatGroq(model="openai/gpt-oss-120b", api_key="my_groq_api_key")
            response = llm("What is Langchain?")
            ```

        Note:
            The class currently supports text-to-text generation only.
        """

        if api_key is None:
            raise InvalidRequest("API key is not given.")

        if model not in GROQ_MODELS:
            raise InvalidRequest(f"Model `{model}` is not allowed, only {list(GROQ_MODELS)} are supported.")

        self.__model = _LangchainChatGroq(model=model,
                                          temperature=temperature,
                                          max_tokens=max_tokens,
                                          base_url=end_point,
                                          api_key=api_key)

        # Saving model initialize parameters
        self.__params : Dict[str, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "end_point" : end_point,  # base_url
        }

    def generate(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            AIMessage: The generated response from Groq.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        if query is None:
            raise InvalidRequest("`query` is given `None`")

        return self.__model.invoke(input=query)

    def get_params(self):
        """Get the parameters used during initialization.

        Returns:
            Dict[str, Any]: A dictionary containing the initialization parameters.
        """
        return self.__params

    """Example:
        model = ChatGroq(model="openai/gpt-oss-120b", api_key="my_groq_api_key")
        response = model("Hello")
    """
    def __call__(self, query : Any = None):
        """Generate response on given `query`. Same as `generate()`."""
        return self.generate(query=query)


if __name__ == "__main__":
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key="groq_key_pls")
    response = llm(query="Hello? How can you help me?")
