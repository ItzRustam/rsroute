# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

# NOTE: gemini client supports ChatModel and Embedding Model both.

"""
NOTE: langchain-google-genai version used = 4.4.0 and langchain update may cause problems to create issues please.

model: Name of the target Gemini model (e.g., "gemini-2.5-flash").

google_api_key: Your Gemini API credential key.

temperature: Randomness control from 0.0 (deterministic) to 2.0.

max_tokens: Maximum token limit for the generated output.

top_p: Nucleus sampling probability threshold for choosing tokens.

top_k: Limits token selection pool to the top K tokens.

thinking_budget: Maximum tokens allocated for internal reasoning chains.

thinking_level: Simple reasoning length toggle ("low", "medium", "high").

safety_settings: Thresholds to block hate speech, harassment, or explicit content.

system_instruction: Base system prompt given directly to the model.

base_url: Custom endpoint URL for proxy servers or API gateways.

additional_headers: Custom HTTP headers attached to every request.

client_args: Lower-level SDK configurations for advanced proxy tuning.

service_tier: Sets processing priority ('standard', 'priority', or 'flex').
"""

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.Errors import *
from typing import Any, Dict, List
from typing import Any, Dict, List
from langchain.messages import AIMessage
from langchain_core.tools import BaseTool
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage, HumanMessage
from rich import print as rprint # useful while debugging
from langchain_core.tools import tool, StructuredTool
import warnings
from app.providers.base import BaseEstimator, BaseEstimatorAgent

"""Class ChatGemini Does not supports `Streaming` & model_kwrags. supports only text-to-text"""

class ChatGemini(BaseEstimator):
    def __init__(
        self,
        api_key : str = None,
        model : str = "gemini-3.5-flash-lite",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        top_p : int = 1.0,

        # Base url
        end_point : str = None,
        thinking_level : str = None,
        thinking_budget : int = None
    ) -> AIMessage:
        # TODO: Doc Strings
        """Integration with Google Gemini via Langchain.

        This class provides a wrapper around Langchain's `ChatGoogleGenerativeAI` to simplify
        interaction with Gemini's model endpoints. It abstracts away the configuration of connection
        settings, model parameters, and query handling.

        Attributes:
            _model (ChatGoogleGenerativeAI): Instance of Langchain's `ChatGoogleGenerativeAI` configured with
                the specified parameters.
            _params (Dict[Any, Any]): Dictionary containing the parameters used to initialize
                the model, useful for debugging or introspection.

        Raises:
            InvalidRequest: If `api_key` is not provided during initialization.

        Example:
            Initialize the Gemini client with a specific model and API key:
            ```python
            llm = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfjysduyrwhjhruwfy_hsdgfhjdf_FAKE_API_KEY_BTW")
            response = llm("What is the capital of France?")
            ```

        Usage:
            - Create an instance of `ChatGemini` with desired parameters.
            - Call the instance like a function to generate responses.
            - Utilize `get_params()` to retrieve the initialization parameters.

        Note:
            The class currently supports text-to-text generation and does not expose
            advanced streaming or additional model keyword arguments.
        """

        super().__init__()
        self._validate_api_key(api_key)

        # Parameter Holding
        self._params : Dict[Any, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "top_p" : top_p,
            "end_point" : end_point,
            "thinking_level" : thinking_level,
            "thinking_budget": thinking_budget
        }

        # Hidden Chat Model
        self._model = ChatGoogleGenerativeAI(model=model,
                                              temperature=temperature,
                                              max_tokens=max_tokens,
                                              top_p=top_p,
                                              base_url=end_point,
                                              thinking_level=thinking_level,
                                              thinking_budget=thinking_budget,
                                              google_api_key=api_key)

        # Backwards compatibility attributes
        self.__model = self._model
        self.__params = self._params

    # auto call
    """Example:
    model = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfu37jhkdflkjhfa73")
    response = model("wtf")
    """
    def __call__(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            str: The generated response from Gemini.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        return self.generate(query=query)


    def generate(self, query : Any = None):
        """Generate response on given `query`.

        Args:
            query (Any): The input prompt or query to generate a response for.

        Returns:
            str: The generated response from Gemini.

        Raises:
            InvalidRequest: If `query` is not provided.
        """
        return super().generate(query=query)

    def get_params(self):
        "Model initialized parameters"
        return super().get_params()


class GeminiAgent(BaseEstimatorAgent):

    def __fake_tool(self, name : str, description : str) -> StructuredTool:
        return self._fake_tool(name=name, description=description)

    def __create_fake_tools(self, tools_info : List[Dict[str, str]]) -> List[StructuredTool]:
        return self._create_fake_tools(tools_info=tools_info)

    def __init__(
        self,
        api_key : str = None,
        model : str = "gemini-3.5-flash-lite",
        temperature : float = 0.7,
        max_tokens : int = 2048,
        top_p : int = 1.0,

        # Base url
        end_point : str = None,
        thinking_level : str = None,
        thinking_budget : int = None,

        tools_info : List[Dict[str, str]] = None
    ) -> AIMessage:
        warnings.warn("For Best Agentic Experience use rsroute python package. https://www.github.com/ItzRustam/rsroute-package")
        super().__init__()
        self._validate_api_key(api_key)
        self._validate_tools_info(tools_info)

        created_tools = self._create_fake_tools(tools_info=tools_info)

        # Parameter Holding
        self._params : Dict[Any, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "top_p" : top_p,
            "end_point" : end_point,
            "thinking_level" : thinking_level,
            "thinking_budget": thinking_budget,
            "binded_tools": tools_info
        }

        # Hidden Agent Model
        self._model = ChatGoogleGenerativeAI(model=model,
                                              temperature=temperature,
                                              max_tokens=max_tokens,
                                              top_p=top_p,
                                              base_url=end_point,
                                              thinking_level=thinking_level,
                                              thinking_budget=thinking_budget,
                                              google_api_key=api_key).bind_tools(tools=created_tools)

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

if __name__ == "__main__":
    llm = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfjysduyrwhjhruwfy_hsdgfhjdf_FAKE_API_KEY_BTW")
    response = llm(query="Hello? How can you help me?")

        