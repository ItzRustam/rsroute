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
from app.providers.base import BaseEstimator

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


class GeminiAgent:

    def __fake_tool(self, name : str, description : str) -> StructuredTool:
        @tool(name, description=description)
        def created_tool():
            ...

        return created_tool

    def __create_fake_tools(self, tools_info : Dict[str, str]) -> List[StructuredTool]:
        """create fake tools"""
        tools : List[StructuredTool] = []

        for tool_info in tools_info:
            if "name" not in tool_info or "description" not in tool_info:
                raise InvalidRequest("Give proper tool functioning `name` and `description`")

            tools.append(self.__fake_tool(name=tool_info.get("name"), description=tool_info.get("description")))

        return tools


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
        """Gemini-powered agentic wrapper with tool-binding support via Langchain.

        Wraps `ChatGoogleGenerativeAI` and binds fake/stub tools to the model,
        enabling the model to reason about and invoke external tools by name.
        Unlike `ChatGemini`, this class is designed for agentic workflows where
        the model decides which tool to call based on the query.

        Args:
            api_key (str): Google Gemini API credential key. Required.
            model (str): Target Gemini model name. Defaults to ``"gemini-3.5-flash-lite"``.
            temperature (float): Creativity/randomness control (0.0–2.0). Defaults to ``0.7``.
            max_tokens (int): Maximum tokens to generate per response. Defaults to ``2048``.
            top_p (float): Nucleus sampling threshold (0.0–1.0). Defaults to ``1.0``.
            end_point (str): Custom base URL for proxy servers or API gateways. Optional.
            thinking_level (str): Reasoning depth toggle — ``"low"``, ``"medium"``, or ``"high"``. Optional.
            thinking_budget (int): Max tokens allocated for internal reasoning chains. Optional.
            tools_info (List[Dict[str, str]]): List of tool definitions to bind to the agent.
                Each entry must have ``"name"`` and ``"description"`` keys. Required.

        Raises:
            InvalidRequest: If ``api_key`` is ``None``.
            InvalidRequest: If ``tools_info`` is ``None``, empty, not a list, or contains non-dict entries.

        Example:
            ```python
            agent = GeminiAgent(
                api_key="YOUR_API_KEY",
                model="gemini-3.5-flash-lite",
                tools_info=[
                    {"name": "search_web", "description": "Search the web for real-time information."},
                    {"name": "calculator",  "description": "Evaluate mathematical expressions."},
                ]
            )
            response = agent("What is 42 * 7 and what's the weather in Paris?")
            ```

        Note:
            Tools are registered as lightweight stubs — the model selects which tool to call
            and returns ``tool_calls`` in the response, but actual tool execution happens
            on the client side. See ``AgentTemplate`` in ``tools.py`` for the response shape.

            Tool info format::

                [
                    {"name": "tool_name", "description": "What this tool does"},
                    ...
                ]
        """

        warnings.warn("For Best Agentic Experience use rsroute python package. https://www.github.com/ItzRustam/rsroute-package")
        
        
        if api_key is None:
            raise InvalidRequest(f"API key is not given.")

        if tools_info is None:
            raise InvalidRequest(f"No Tool given to Agent Edition")
        
        if not(isinstance(tools_info, list)):
            raise InvalidRequest("Tools must follow the order. [{'name' : 'name of tool', 'description': 'description of tool'}]")

        if len(tools_info) == 0:
            raise InvalidRequest("No tool provided")
        
        if not(isinstance(tools_info[0], dict)):
            raise InvalidRequest("Tools are Provided in wrong Format use Dict.")

        created_tools = self.__create_fake_tools(tools_info=tools_info)

        # Parameter Holding
        self.__params : Dict[Any, Any] = {
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
        self.__agent = ChatGoogleGenerativeAI(model=model,
                                              temperature=temperature,
                                              max_tokens=max_tokens,
                                              top_p=top_p,
                                              base_url=end_point,
                                              thinking_level=thinking_level,
                                              thinking_budget=thinking_budget,
                                              google_api_key=api_key).bind_tools(tools=created_tools)

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
        if query is None:
            raise InvalidRequest(f"`query` is given `None`")

        return self.__agent.invoke(input=query)

    def get_params(self):
        "Model initialized parameters"
        return self.__params

if __name__ == "__main__":
    llm = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfjysduyrwhjhruwfy_hsdgfhjdf_FAKE_API_KEY_BTW")
    response = llm(query="Hello? How can you help me?")

        