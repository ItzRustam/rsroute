# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test running FastAPI server"""
from app.server import create_server
import requests as rq
from pprint import pprint

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

URL = "http://0.0.0.0:8000" 
DATA = {"query" : "What is GitHub?", 
        "master_key": "RSRoute_my_key", 
        "model": "gemini-3.5-flash-lite", 
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None, 
        "thinking_level": None,
        "thinking_budget": None}

# Without Master Key (WMK) or Wrong Master Key
DATA_WMK = {"query" : "Hello?", 
        "master_key": "dsfjkhsdf,sdaf", 
        "model": "gemini-3.5-flash-lite", 
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None, 
        "thinking_level": None,
        "thinking_budget": None}


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
        response = rq.post(url=f"{URL}/v1/gemini/chat", params=DATA)
        return check_status(status_code=response.status_code), response.json()

    @staticmethod
    def check_gemini_without_key():
        response = rq.post(url=f"{URL}/v1/gemini/chat", params=DATA_WMK)
        return check_status(status_code=response.status_code), response.json()

if __name__ == "__main__":
    status, output = check_server.check_gemini_with_key()
    print(status)
    pprint(output)
    
        