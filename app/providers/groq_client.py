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
from typing import Any, Dict, List, Optional
import warnings
from app.providers.base import BaseChatModel, BaseAgentModel
from app.defaults import DEFAULT_GROQ_MODEL, MAX_TOKENS, TEMPERATURE, MAX_RETRIES

"""Class ChatGroq Does not supports `Streaming` & model_kwargs. supports only text-to-text"""
class ChatGroq(BaseChatModel):
    def __init__(
        self,
        api_key : str = None,
        model : str = DEFAULT_GROQ_MODEL,
        temperature : float = TEMPERATURE,
        max_tokens : int = MAX_TOKENS,
        max_retries : int = MAX_RETRIES,

        # Base url
        end_point : str = None,
    ):
        """Integration with Groq via Langchain.

        This class provides a wrapper around Langchain's `ChatGroq` to simplify
        interaction with Groq's model endpoints.

        Attributes:
            _model (_LangchainChatGroq): Instance of Langchain's `ChatGroq` configured with
                the specified parameters.
            _params (Dict[str, Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Raises:
            InvalidRequest: If `api_key` is not provided.

        Example:
            ```python
            llm = ChatGroq(model="openai/gpt-oss-120b", api_key="my_groq_api_key")
            response = llm("What is Langchain?")
            ```

        Note:
            The class currently supports text-to-text generation only.
        """
        super().__init__()
        self._validate_api_key(api_key)

        self._model = _LangchainChatGroq(model=model,
                                          temperature=temperature,
                                          max_tokens=max_tokens,
                                          base_url=end_point,
                                          max_retries=max_retries,
                                          api_key=api_key)

        # Saving model initialize parameters
        self._params : Dict[str, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "max_retries" : max_retries,
            "end_point" : end_point,  # base_url
        }

        # Backwards compatibility attributes
        self.__model = self._model
        self.__params = self._params



class GroqAgent(BaseAgentModel):
    def __init__(
        self,
        api_key : str = None,
        model : str = DEFAULT_GROQ_MODEL,
        temperature : float = TEMPERATURE,
        max_tokens : int = MAX_TOKENS,
        max_retries : int = MAX_RETRIES,

        # Base url
        end_point : str = None,

        tools_info : List[Dict[str, str]] = None
    ):
        """Groq-powered agentic wrapper with tool-binding support via Langchain.

        Wraps `ChatGroq` and binds fake/stub tools to the model,
        enabling the model to reason about and invoke external tools by name.

        Args:
            api_key (str): Groq API credential key. Required.
            model (str): Target Groq model name. Defaults to ``"openai/gpt-oss-120b"``.
            temperature (float): Creativity/randomness control (0.0–2.0). Defaults to ``0.7``.
            max_tokens (int): Maximum tokens to generate per response. Defaults to ``2048``.
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
            "max_retries" : max_retries,
            "end_point" : end_point,
            "binded_tools": tools_info,
        }

        self._model = _LangchainChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=end_point,
            max_retries=max_retries,
            api_key=api_key
        ).bind_tools(tools=created_tools)

        self.__agent = self._model
        self.__params = self._params



if __name__ == "__main__":
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key="groq_key_pls")
    response = llm(query="Hello? How can you help me?")
