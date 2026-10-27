# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Base estimator module for RSRoute providers."""

from abc import ABC
from typing import Any, Dict, Optional
from app.Errors import InvalidRequest


class BaseEstimator(ABC):
    """Abstract base estimator class for LLM providers in RSRoute.

    Provides common parameter management, validation, and generation interfaces
    across all provider clients (ChatGroq, ChatGemini, ChatMistralAI).

    Attributes:
        _model: The underlying LangChain chat model or runnable instance.
        _params (Dict[str, Any]): Dictionary containing initialization parameters.
    """

    def __init__(self, **kwargs):
        self._params: Dict[str, Any] = {}
        self._model: Any = None

    def _validate_api_key(self, api_key: Optional[str]) -> None:
        """Validate that an API key was provided.

        Raises:
            InvalidRequest: If `api_key` is None.
        """
        if api_key is None:
            raise InvalidRequest("API key is not given.")

    def _validate_query(self, query: Any) -> None:
        """Validate that a query was provided.

        Raises:
            InvalidRequest: If `query` is None.
        """
        if query is None:
            raise InvalidRequest("`query` is given `None`")

    def generate(self, query: Any = None) -> Any:
        """Generate a response for the given query.

        Args:
            query (Any): The input prompt or query.

        Returns:
            Any: The response from the underlying model.

        Raises:
            InvalidRequest: If `query` is None or model is not initialized.
        """
        self._validate_query(query)
        model = self._model
        if model is None:
            # Fallback to private attribute if defined in subclasses
            model = getattr(self, f"_{self.__class__.__name__}__model", None)
            if model is None:
                model = getattr(self, f"_{self.__class__.__name__}__agent", None)
        if model is None:
            raise InvalidRequest("Model is not initialized.")
        return model.invoke(input=query)

    def __call__(self, query: Any = None) -> Any:
        """Generate response on given `query`. Same as `generate()`."""
        return self.generate(query=query)

    def get_params(self) -> Dict[str, Any]:
        """Get the parameters used during initialization.

        Returns:
            Dict[str, Any]: A dictionary containing the initialization parameters.
        """
        if self._params:
            return self._params
        mangled = getattr(self, f"_{self.__class__.__name__}__params", None)
        if mangled is not None:
            return mangled
        return {}

    def set_params(self, **params) -> "BaseEstimator":
        """Set parameters for this estimator.

        Args:
            **params: Parameter names and values to update.

        Returns:
            self: The estimator instance.
        """
        self._params.update(params)
        return self

