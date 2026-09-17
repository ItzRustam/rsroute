# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Test running FastAPI server"""
from app.server import create_server
import requests as rq

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
DATA = {"query" : "Hello?"}

def check_status(status_code):
    if int(status_code) == 200:
        return True
    else:
        return False

class check_server:
    """
    Server Checker
    --------------

    Check server on ``URL`` & ``DATA``

    Available Routes Test
    ----------------------
    * Gemini
    """

    @staticmethod
    def check_gemini():
        response = rq.post(url=f"{URL}/v1/gemini/chat", data=DATA)
        return check_status(status_code=response.status_code), response.json()

if __name__ == "__main__":
    status, output = check_server.check_gemini()
    print(status)
    print(output)
        