# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from app.providers import ChatOpenRouter
from app.Errors import InvalidRequest

"NOTE: Test Function only on Fake API_KEY, Already tested on Real OpenRouter API key."
def test_openrouter(KEY : str = None, query : str = None, real_api = False):
    # Model Initialize
    try:
        model = ChatOpenRouter(api_key=KEY)
    except InvalidRequest as ir:
        return True, ir
    except Exception as e:
        return False, e

    try:
        output = model(query=query)
    except InvalidRequest as ir:
        return True, ir
    except Exception as e:
        if real_api:
            return False, e
        return True, e
    else:
        if not real_api:
            return False, "Unexpected Error Occur."
        return True, output

