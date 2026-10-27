# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Base estimator module for RSRoute providers."""

from abc import ABC
from typing import Any, Dict, List, Optional
import warnings
from langchain_core.tools import tool, StructuredTool
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

    def _validate_api_key(self, api_key: Optional[str] = None) -> None:
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


class BaseEstimatorAgent(BaseEstimator):
    """Abstract base estimator class for agentic LLM providers in RSRoute.

    Wraps chat models with tool-binding support via Langchain,
    enabling agentic workflows where models reason about and select tools to invoke.

    Attributes:
        _model: The underlying LangChain model with tools bound.
        _params (Dict[str, Any]): Dictionary containing initialization parameters.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _fake_tool(self, name: str, description: str) -> StructuredTool:
        """Create a stub StructuredTool with given name and description."""
        @tool(name, description=description)
        def created_tool():
            ...
        return created_tool

    def _create_fake_tools(self, tools_info: List[Dict[str, str]]) -> List[StructuredTool]:
        """Create fake/stub tools from tool info dictionaries."""
        tools: List[StructuredTool] = []
        for tool_info in tools_info:
            if not isinstance(tool_info, dict) or "name" not in tool_info or "description" not in tool_info:
                raise InvalidRequest("Give proper tool functioning `name` and `description`")
            tools.append(self._fake_tool(name=tool_info.get("name"), description=tool_info.get("description")))
        return tools

    def _validate_tools_info(self, tools_info: Any) -> None:
        """Validate tools_info structure.

        Raises:
            InvalidRequest: If tools_info is None, empty, not a list, or contains non-dict entries.
        """
        if tools_info is None:
            raise InvalidRequest("No Tool given to Agent Edition")

        if not isinstance(tools_info, list):
            raise InvalidRequest("Tools must follow the order. [{'name' : 'name of tool', 'description': 'description of tool'}]")

        if len(tools_info) == 0:
            raise InvalidRequest("No tool provided")

        if not isinstance(tools_info[0], dict):
            raise InvalidRequest("Tools are Provided in wrong Format use Dict.")

        for tool_info in tools_info:
            if not isinstance(tool_info, dict) or "name" not in tool_info or "description" not in tool_info:
                raise InvalidRequest("Give proper tool functioning `name` and `description`")

    # Compatibility aliases for previous private methods
    def _BaseEstimatorAgent__fake_tool(self, name: str, description: str) -> StructuredTool:
        return self._fake_tool(name=name, description=description)

    def _BaseEstimatorAgent__create_fake_tools(self, tools_info: List[Dict[str, str]]) -> List[StructuredTool]:
        return self._create_fake_tools(tools_info=tools_info)


