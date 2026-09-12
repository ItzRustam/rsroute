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
from typing import Any, Dict

"""Class ChatGemini Does not supports `Streaming` & model_kwrags. supports only text-to-text"""

class ChatGemini:
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
    ):
        # TODO: Doc Strings

        if api_key is None:
            raise InvalidRequest(f"API key is not given.")

        # Parameter Holding
        self.__params : Dict[Any, Any] = {
            "model" : model,
            "temperature" : temperature,
            "max_tokens" : max_tokens,
            "top_p" : top_p,
            "end_point" : end_point,
            "thinking_level" : thinking_level,
            "thinking_budget": thinking_budget
        }

        # Hidden Chat Model
        self.__model = ChatGoogleGenerativeAI(model=model,
                                              temperature=temperature,
                                              max_tokens=max_tokens,
                                              top_p=top_p,
                                              base_url=end_point,
                                              thinking_level=thinking_level,
                                              thinking_budget=thinking_budget,
                                              google_api_key=api_key)

    # auto call
    """Example:
    model = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfu37jhkdflkjhfa73")
    response = model("wtf")
    """
    def __call__(self, query : Any = None):
        """Generate response on given `query`"""
        return self.generate(query=query)

    def generate(self, query : Any = None):
        """Generate response on given `query`"""
        if query is None:
            raise InvalidRequest(f"`query` is given `None`")

        return self.__model.invoke(input=query)

    def get_params(self):
        "Model initialized parameters"
        return self.__params


if __name__ == "__main__":
    llm = ChatGemini(model="gemini-3.5-flash-lite", api_key="AQ.kjhdfjysduyrwhjhruwfy_hsdgfhjdf_FAKE_API_KEY_BTW")
    response = llm(query="Hello? How can you help me?")

        