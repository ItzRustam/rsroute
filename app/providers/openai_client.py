# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""This File Contains rsroute integration with OpenAI using Langchain."""

from langchain_openai import ChatOpenAI as _LangchainChatOpenAI
from app.Errors import *
from typing import Any, Dict, List, Optional
import warnings
from app.providers.base import BaseChatModel, BaseAgentModel
from app.defaults import OPENAI_DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS, TIMEOUT, MAX_RETRIES
from langchain_core.messages import AIMessage
from langchain_core.tools import tool, StructuredTool

"""Class ChatOpenAI Does not supports `Streaming` & model_kwargs. supports only text-to-text"""
class ChatOpenAI(BaseChatModel):
    def __init__(
        self,
        api_key: str = None,
        model: str = OPENAI_DEFAULT_MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        max_retries: int = MAX_RETRIES,
        timeout: int = TIMEOUT,
        use_response_api: bool = False,

        # Base url
        end_point: str = None,

        # Organization
        organization_id: str = None,
    ) -> AIMessage:
        """Integration with OpenAI via Langchain.

        This class provides a wrapper around Langchain's `ChatOpenAI` to simplify
        interaction with OpenAI's model endpoints. It abstracts away the configuration
        of connection settings, model parameters, and query handling.

        Attributes:
            _model (_LangchainChatOpenAI): Instance of Langchain's `ChatOpenAI` configured with
                the specified parameters.
            _params (Dict[str, Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Args:
            api_key (str): OpenAI API credential key. Required.
            model (str): Target OpenAI model name. Defaults to ``"gpt-6-luna"``.
            temperature (float): Creativity/randomness control (0.0-2.0). Defaults to ``0.7``.
            max_tokens (int): Maximum tokens to generate per response. Defaults to ``4096``.
            max_retries (int): Number of automated retries on transient failures. Defaults to ``2``.
            timeout (int): Network request timeout in seconds. Defaults to ``60``.
            use_response_api (bool): Whether to use the OpenAI Responses API instead of Chat
                Completions. Defaults to ``False``.
            end_point (str): Custom base URL for proxy servers or API gateways. Optional.
            organization_id (str): OpenAI organization identifier. Optional.

        Raises:
            InvalidRequest: If ``api_key`` is not provided during initialization.

        Example:
            Initialize the OpenAI client with a specific model and API key:
            ```python
            llm = ChatOpenAI(model="gpt-6-luna", api_key="sk-proj-FAKE_API_KEY_BTW")
            response = llm("What is the capital of France?")
            ```

        Usage:
            - Create an instance of ``ChatOpenAI`` with desired parameters.
            - Call the instance like a function to generate responses.
            - Utilize ``get_params()`` to retrieve the initialization parameters.

        Note:
            The class currently supports text-to-text generation and does not expose
            advanced streaming or additional model keyword arguments.
        """
        super().__init__()
        self._validate_api_key(api_key)

        # Hidden Chat Model
        self._model = _LangchainChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            timeout=timeout,
            use_responses_api=use_response_api,
            base_url=end_point,
            organization=organization_id,
        )

        # Parameter Holding
        self._params: Dict[str, Any] = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "max_retries": max_retries,
            "timeout": timeout,
            "use_response_api": use_response_api,
            "end_point": end_point,
        }

        # Backwards compatibility attributes
        self.__model = self._model
        self.__params = self._params


class OpenAIAgent(BaseAgentModel):
    """OpenAI-powered agentic wrapper with tool-binding support via Langchain.

    Wraps `ChatOpenAI` and binds fake/stub tools to the model,
    enabling the model to reason about and invoke external tools by name.

    Attributes:
        _model: Instance of Langchain's `ChatOpenAI` with tools bound.
        _params (Dict[str, Any]): Dictionary containing the parameters used to initialize
            the model, useful for debugging or introspection.

    Raises:
        InvalidRequest: If ``api_key`` is not provided during initialization.
        InvalidRequest: If ``tools_info`` is not provided, empty, or incorrectly formatted.

    Example:
        ```python
        tools = [{"name": "web_search", "description": "Search the web"}]
        agent = OpenAIAgent(
            api_key="sk-proj-FAKE_KEY",
            tools_info=tools
        )
        response = agent("What is the weather today?")
        ```
    """

    def __fake_tool(self, name: str, description: str) -> StructuredTool:
        return self._fake_tool(name=name, description=description)

    def __create_fake_tools(self, tools_info: List[Dict[str, str]]) -> List[StructuredTool]:
        return self._create_fake_tools(tools_info=tools_info)

    def __init__(
        self,
        api_key: str = None,
        model: str = OPENAI_DEFAULT_MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        max_retries: int = MAX_RETRIES,
        timeout: int = TIMEOUT,
        use_response_api: bool = False,

        # Base url
        end_point: str = None,

        # Organization
        organization_id: str = None,

        tools_info: List[Dict[str, str]] = None,
    ) -> AIMessage:
        """OpenAI-powered agentic wrapper with tool-binding support via Langchain.

        Args:
            api_key (str): OpenAI API credential key. Required.
            model (str): Target OpenAI model name. Defaults to ``"gpt-6-luna"``.
            temperature (float): Creativity/randomness control (0.0–2.0). Defaults to ``0.7``.
            max_tokens (int): Maximum tokens to generate per response. Defaults to ``4096``.
            max_retries (int): Number of automated retries on transient failures. Defaults to ``2``.
            timeout (int): Network request timeout in seconds. Defaults to ``60``.
            use_response_api (bool): Whether to use the OpenAI Responses API instead of Chat
                Completions. Defaults to ``False``.
            end_point (str): Custom base URL for proxy servers or API gateways. Optional.
            organization_id (str): OpenAI organization identifier. Optional.
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

        # Parameter Holding
        self._params: Dict[str, Any] = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "max_retries": max_retries,
            "timeout": timeout,
            "use_response_api": use_response_api,
            "end_point": end_point,
            "binded_tools": tools_info,
        }

        # Hidden Agent Model
        self._model = _LangchainChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            timeout=timeout,
            use_responses_api=use_response_api,
            base_url=end_point,
            organization=organization_id,
        ).bind_tools(tools=created_tools)

        self.__agent = self._model
        self.__params = self._params

    def __call__(self, query: Any = None):
        """Generate response on given `query`. Same as `generate()`."""
        return self.generate(query=query)

    def generate(self, query: Any = None):
        """Generate response on given `query`."""
        return super().generate(query=query)

    def get_params(self):
        """Model initialized parameters."""
        return super().get_params()


ChatOpenAIAgent = OpenAIAgent
