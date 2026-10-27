# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test running FastAPI server"""
import os

from app.server import create_server
import requests as rq
from rich import print as pprint # pretty print
from typing import Dict, List, Any
from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """Search the web using DuckDuckGo Search (DDGS).

    Args:
        query (str): The search query.
        max_results (int): Maximum number of search results to return.

    Returns:
        List[Dict[str, Any]]: Search results containing title, href, and body.
    """
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return [{"error": str(e)}]


WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the web using DuckDuckGo Search (DDGS) to find current info and websites."
}

"""
NOTE:
Currently This is just a testing code,
server running path & server getting parameter will be changed.

currently includes:
query: str -> prompt

will be added soon:
master_key,
max_token,
temperature,
top_p,
base_url

some special parameter to diffrent providers

GOOGLE
------
thinking_budget,
thinking_level,
safety_settings
"""

URL = f"http://{os.getenv('HOST', '127.0.0.1')}:{os.getenv('PORT', '8000')}"
DATA = {"query" : "What is GitHub?", 
        "master_key": "RSRoute_my_key", 
        "model": "gemini-3.5-flash-lite",
        "temperature" : 0.7,
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None,
        "thinking_level": None,
        "thinking_budget": None
        }

# Without Master Key (WMK) or Wrong Master Key
DATA_WMK = {"query" : "Hello?", 
        "master_key": "RSRoute_WRONG_KEY",
        "model": "gemini-3.5-flash-lite",
        "temperature" : 0.7,
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None, 
        "thinking_level": None,
        "thinking_budget": None}

AGENT_DATA = {
    "query": "What is the latest release of Python?",
    "master_key": "RSRoute_my_key",
    "model": "gemini-3.5-flash-lite",
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 1.0,
    "end_point": None,
    "thinking_level": None,
    "thinking_budget": None,
    "tools_info": [WEB_SEARCH_TOOL]
}

AGENT_DATA_WMK = {
    "query": "What is the latest release of Python?",
    "master_key": "RSRoute_WRONG_KEY",
    "model": "gemini-3.5-flash-lite",
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 1.0,
    "end_point": None,
    "thinking_level": None,
    "thinking_budget": None,
    "tools_info": [WEB_SEARCH_TOOL]
}

END_POINTS : Dict[str, str] = {
    "gemini" : f"{URL}/v1/gemini",
    "mistral" : f"{URL}/v1/mistral",
    "groq" : f"{URL}/v1/groq",
}


def check_status(status_code):
    if int(status_code) == 200:
        return True
    else:
        return False

class check_server:
    """
    Server Checker
    --------------

    Checks server on ``URL`` & ``DATA``

    Available Routes Test
    ----------------------
    * Gemini (Chat & Agent)
    * MistralAI (Chat & Agent)
    * Groq (Chat & Agent)
    """

    @staticmethod
    def check_gemini_with_key():
        response = rq.post(url=f"{END_POINTS['gemini']}/chat", params=DATA)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_gemini_without_key():
        response = rq.post(url=f"{END_POINTS['gemini']}/chat", params=DATA_WMK)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_gemini_agent_with_key():
        response = rq.post(url=f"{END_POINTS['gemini']}/agent", json=AGENT_DATA)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_gemini_agent_without_key():
        response = rq.post(url=f"{END_POINTS['gemini']}/agent", json=AGENT_DATA_WMK)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_mistral_with_key():
        data = DATA.copy()
        # Deleting useless parameter
        del data["thinking_budget"]
        del data["thinking_level"]
        response = rq.post(url=f"{END_POINTS['mistral']}/chat", params=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_mistral_without_key():
        data = DATA_WMK.copy()
        # Deleting useless parameter
        del data["thinking_budget"]
        del data["thinking_level"]
        response = rq.post(url=f"{END_POINTS['mistral']}/chat", params=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_mistral_agent_with_key():
        data = AGENT_DATA.copy()
        del data["thinking_budget"]
        del data["thinking_level"]
        data["model"] = "mistral-small-2603"
        response = rq.post(url=f"{END_POINTS['mistral']}/agent", json=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_mistral_agent_without_key():
        data = AGENT_DATA_WMK.copy()
        del data["thinking_budget"]
        del data["thinking_level"]
        data["model"] = "mistral-small-2603"
        response = rq.post(url=f"{END_POINTS['mistral']}/agent", json=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_groq_with_key():
        data = DATA.copy()
        # Deleting useless parameter
        del data["thinking_budget"]
        del data["thinking_level"]
        del data["top_p"]
        data["model"] = "openai/gpt-oss-120b"
        response = rq.post(url=f"{END_POINTS['groq']}/chat", params=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_groq_without_key():
        data = DATA_WMK.copy()
        # Deleting useless parameter
        del data["thinking_budget"]
        del data["thinking_level"]
        del data["top_p"]
        data["model"] = "openai/gpt-oss-120b"
        response = rq.post(url=f"{END_POINTS['groq']}/chat", params=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_groq_agent_with_key():
        data = AGENT_DATA.copy()
        del data["thinking_budget"]
        del data["thinking_level"]
        del data["top_p"]
        data["model"] = "openai/gpt-oss-120b"
        response = rq.post(url=f"{END_POINTS['groq']}/agent", json=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_groq_agent_without_key():
        data = AGENT_DATA_WMK.copy()
        del data["thinking_budget"]
        del data["thinking_level"]
        del data["top_p"]
        data["model"] = "openai/gpt-oss-120b"
        response = rq.post(url=f"{END_POINTS['groq']}/agent", json=data)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_gemini_params():
        response = rq.get(url=f"{END_POINTS['gemini']}/parameter")
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_mistral_params():
        response = rq.get(url=f"{END_POINTS['mistral']}/parameter")
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_groq_params():
        response = rq.get(url=f"{END_POINTS['groq']}/parameters")
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_root():
        response = rq.get(url=f"{URL}/")
        return check_status(status_code=response.status_code), response.json()


if __name__ == "__main__":
    """Use Function to check server."""
    # Root check
    status, output = check_server.check_root()
    print("Root status:", status)
    pprint(output)

    # Gemini Chat checks
    status, output = check_server.check_gemini_with_key()
    print("Gemini Chat with key:", status)
    pprint(output)

    status, output = check_server.check_gemini_without_key()
    print("Gemini Chat without key:", status)
    pprint(output)

    # Gemini Agent checks (using web_search tool with DDGS)
    status, output = check_server.check_gemini_agent_with_key()
    print("Gemini Agent with key:", status)
    pprint(output)

    status, output = check_server.check_gemini_agent_without_key()
    print("Gemini Agent without key:", status)
    pprint(output)

    status, output = check_server.check_gemini_params()
    print("Gemini params:", status)
    pprint(output)

    # MistralAI Chat checks
    status, output = check_server.check_mistral_with_key()
    print("Mistral Chat with key:", status)
    pprint(output)

    status, output = check_server.check_mistral_without_key()
    print("Mistral Chat without key:", status)
    pprint(output)

    # MistralAI Agent checks (using web_search tool with DDGS)
    status, output = check_server.check_mistral_agent_with_key()
    print("Mistral Agent with key:", status)
    pprint(output)

    status, output = check_server.check_mistral_agent_without_key()
    print("Mistral Agent without key:", status)
    pprint(output)

    status, output = check_server.check_mistral_params()
    print("Mistral params:", status)
    pprint(output)

    # Groq Chat checks
    status, output = check_server.check_groq_with_key()
    print("Groq Chat with key:", status)
    pprint(output)

    status, output = check_server.check_groq_without_key()
    print("Groq Chat without key:", status)
    pprint(output)

    # Groq Agent checks (using web_search tool with DDGS)
    status, output = check_server.check_groq_agent_with_key()
    print("Groq Agent with key:", status)
    pprint(output)

    status, output = check_server.check_groq_agent_without_key()
    print("Groq Agent without key:", status)
    pprint(output)

    status, output = check_server.check_groq_params()
    print("Groq params:", status)
    pprint(output)
