# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from langchain_openrouter import ChatOpenRouter  as _LangchainChatOpenRouter
from app.Errors import *
from typing import Any, Dict, List, Optional
from langchain_core.messages import AIMessage
from langchain_core.tools import tool, StructuredTool
import warnings
from app.providers.base import BaseChatModel, BaseAgentModel
from app.defaults import DEFAULT_OPENROUTER_MODEL, MAX_TOKENS, TEMPERATURE

class ChatOpenRouter(BaseChatModel):
    """Integration with OpenRouter via Langchain.

    This class provides a wrapper around Langchain's `ChatOpenRouter` to simplify
    interaction with OpenRouter's model endpoints. It abstracts away the configuration
    of connection settings, model parameters, provider preferences, and query handling.

    Attributes:
        _model (ChatOpenRouter): Instance of Langchain's `ChatOpenRouter` configured
            with the specified parameters.
        _params (Dict[str, Any]): Dictionary containing the parameters used to initialize
            the model, useful for debugging or introspection.

    Raises:
        InvalidRequest: If `api_key` is not provided during initialization.

    Example:
        Initialize the OpenRouter client with a specific model and API key:
        ```python
        llm = ChatOpenRouter(model="openai/gpt-4o-mini", api_key="sk-or-v1-FAKE_API_KEY_BTW")
        response = llm("What is the capital of France?")
        ```

    Usage:
        - Create an instance of `ChatOpenRouter` with desired parameters.
        - Call the instance like a function to generate responses.
        - Utilize `get_params()` to retrieve the initialization parameters.
        - Pass `providers` to set OpenRouter provider preferences.
        - Pass `**model_kwargs` to forward additional model-specific arguments.

    Note:
        This class supports `model_kwargs` for extended model configuration but
        does not currently support streaming.
    """
    def __init__(
        self,
        api_key : str = None,
        model : str = DEFAULT_OPENROUTER_MODEL,
        temperature : float = TEMPERATURE,
        max_tokens : int = MAX_TOKENS,
        app_title : str = "RSRoute",
        app_url : str = "https://www.rsroute.freedev.app/",
        app_categories : List[str] = None,
        max_retries : int = 2,

        # provider preferences
        providers : Dict[Any, Any] = None,

        # Base url
        end_point : str = None,
        **model_kwargs
    ) -> AIMessage:
        super().__init__()
        self._validate_api_key(api_key=api_key)

        # model
        self._model = _LangchainChatOpenRouter(model=model,
                                               api_key=api_key,
                                               temperature=temperature,
                                               max_tokens=max_tokens,
                                               base_url=end_point,
                                               app_title=app_title,
                                               app_url=app_url,
                                               app_categories=app_categories,
                                               max_retries=max_retries,
                                               openrouter_provider=providers,
                                               model_kwargs=model_kwargs)

        self._params : Dict[str, Any] = {
            "model":model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "app_url" : app_url,
            "app_title": app_title,
            "app_categories" : app_categories,
            "max_retries" : max_retries,
            "openrouter_provider": providers,
            "end_point" : end_point,

            "model_kwargs": model_kwargs
        }

        # Backwards compatibility attributes
        self.__model = self._model
        self.__params = self._params


class OpenRouterAgent(BaseAgentModel):
    """OpenRouter-powered agentic wrapper with tool-binding support via Langchain.

    Wraps `ChatOpenRouter` and binds fake/stub tools to the model,
    enabling the model to reason about and invoke external tools by name.

    Attributes:
        _model: Instance of Langchain's `ChatOpenRouter` with tools bound.
        _params (Dict[str, Any]): Dictionary containing the parameters used to initialize
            the model, useful for debugging or introspection.

    Raises:
        InvalidRequest: If `api_key` is not provided during initialization.
        InvalidRequest: If `tools_info` is not provided, empty, or incorrectly formatted.

    Example:
        ```python
        tools = [{"name": "web_search", "description": "Search the web"}]
        agent = OpenRouterAgent(
            api_key="sk-or-v1-FAKE_KEY",
            tools_info=tools
        )
        response = agent("What is the weather today?")
        ```
    """

    def __fake_tool(self, name : str, description : str) -> StructuredTool:
        return self._fake_tool(name=name, description=description)

    def __create_fake_tools(self, tools_info : List[Dict[str, str]]) -> List[StructuredTool]:
        return self._create_fake_tools(tools_info=tools_info)

    def __init__(
        self,
        api_key : str = None,
        model : str = DEFAULT_OPENROUTER_MODEL,
        temperature : float = TEMPERATURE,
        max_tokens : int = MAX_TOKENS,
        app_title : str = "RSRoute",
        app_url : str = "https://www.rsroute.freedev.app/",
        app_categories : List[str] = None,
        max_retries : int = 2,

        # provider preferences
        providers : Dict[Any, Any] = None,

        # Base url
        end_point : str = None,

        tools_info : List[Dict[str, str]] = None,
        **model_kwargs
    ) -> AIMessage:
        warnings.warn("For Best Agentic Experience use rsroute python package. https://www.github.com/ItzRustam/rsroute-package")
        super().__init__()
        self._validate_api_key(api_key=api_key)
        self._validate_tools_info(tools_info)

        created_tools = self._create_fake_tools(tools_info=tools_info)

        # Parameter Holding
        self._params : Dict[str, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "app_url" : app_url,
            "app_title" : app_title,
            "app_categories" : app_categories,
            "max_retries" : max_retries,
            "openrouter_provider" : providers,
            "end_point" : end_point,
            "binded_tools" : tools_info,
            "model_kwargs" : model_kwargs
        }

        # Hidden Agent Model
        self._model = _LangchainChatOpenRouter(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=end_point,
            app_title=app_title,
            app_url=app_url,
            app_categories=app_categories,
            max_retries=max_retries,
            openrouter_provider=providers,
            model_kwargs=model_kwargs
        ).bind_tools(tools=created_tools)

        self.__agent = self._model
        self.__params = self._params

    def __call__(self, query : Any = None):
        """Generate response on given `query`. Same as `generate()`."""
        return self.generate(query=query)

    def generate(self, query : Any = None):
        """Generate response on given `query`."""
        return super().generate(query=query)

    def get_params(self):
        """Model initialized parameters."""
        return super().get_params()


ChatOpenRouterAgent = OpenRouterAgent


if __name__ == "__main__":
    llm = ChatOpenRouter(model="openai/gpt-4o-mini", api_key="sk-or-v1-fake_key")
    response = llm(query="Hello? How can you help me?")
