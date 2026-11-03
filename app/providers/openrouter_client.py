# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from langchain_openrouter import ChatOpenRouter  as _LangchainChatOpenRouter
from app.Errors import *
from typing import Any, Dict, List, Optional
from langchain_core.messages import AIMessage
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
