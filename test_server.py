# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test running FastAPI server"""
import os

from app.server import create_server
import requests as rq
from rich import print as pprint # pretty print
from typing import Dict

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

URL = f"http://{os.getenv('HOST')}:{os.getenv('PORT')}"
DATA = {"query" : "What is GitHub?", 
        "master_key": "RSRoute_my_key", 
        "model": "gemini-3.5-flash-lite",
        "temperature" : 0.7,
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None, 
        "thinking_level": None,
        "thinking_budget": None}

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

END_POINTS : Dict[str, str] = {
    "gemini" : f"{URL}/v1/gemini",
    "mistral" : f"{URL}/v1/mistral",
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
    * Gemini
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


if __name__ == "__main__":
    """Use Function to check server."""
    status, output = check_server.check_gemini_without_key()
    print(status)
    pprint(output)

    status, output = check_server.check_mistral_without_key()
    print(status)
    pprint(output)

    status, output = check_server.check_mistral_with_key()
    print(status)
    pprint(output)