# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"Authrectication for Master_key if ENABLE_AUTH=TRUE"

from dotenv import load_dotenv
import os
from app.Errors import *
load_dotenv()

def auth_exits() -> bool:
    auth_enabled = os.getenv("ENABLE_AUTH", "false").lower() == "true"
    return auth_enabled

def auth(master_key : str = None) -> bool:
    if master_key is None:
        raise AuthenticationError("Invalid `master_key`, `None`")
    
    if not(master_key.startswith("RSRoute_")):
        raise InvalidMasterKey("given master_key should start with `RSRoute_`.")
    
    # Will handle not start RSRoute_ & Empty Password both at once.
    if not(os.getenv("RSRoute_MASTER_KEY").startswith("RSRoute_")):
        raise InvalidMasterKey("Master Key is not started with `RSRoute_`, try to edit `.env`")
    
    if len(os.getenv("RSRoute_MASTER_KEY")) < 12:
        raise InvalidMasterKey("Master Key can't be smaller than 6. (12)")
    
    if master_key == os.getenv("RSRoute_MASTER_KEY"):
        return True # Able to Login.
    else:
        raise AuthenticationError("Invalid `master_key`. Input correct `master_key`")
    


