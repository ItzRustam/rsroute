# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"Test file for Authrentication"

"""
Note: In the server `auth()` will only called when ENABLE_AUTH=true
"""
import os
from app.auth import auth_exits, auth

def auth_test(master_key=None, return_ = True):
    if not(auth_exits()):
        print("Auth not Enabled.")
    
    try:
        output = auth(master_key=master_key)
        if output:
            if return_:
                return "Auth Done."
            else:
                print("Auth Done.")
        else:
            if return_:
                return "Auth Error"
            else:
                print("Auth Error")
    except Exception as e:
        if return_:
            return e
        else:
            print(e)
