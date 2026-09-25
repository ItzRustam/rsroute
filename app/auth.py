# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Authentication utilities for RSRoute.

Provides functions to check if authentication is enabled globally and to verify a given
master key against the configured master key.
"""


import os
from app.Errors import *

def auth_exits() -> bool:
    """
    Determine if authentication is enabled.

    Returns:
        bool: ``True`` if `ENABLE_AUTH` environment variable is set to ``true`` (case-insensitive);
        otherwise ``False``.
    """

    auth_enabled = os.getenv("ENABLE_AUTH", "false").lower() == "true"
    return auth_enabled

def auth(master_key : str = None) -> bool:
    """
    Verify the provided master key against the configured master key.

    Args:
        master_key (str, optional): The master key to authenticate. Must start with ``RSRoute_``.
            If not provided, raises ``AuthenticationError``.
    
    Returns:
        bool: ``True`` if the provided `master_key` matches the configured ``RSRoute_MASTER_KEY``.
    
    Raises:
        AuthenticationError: When `master_key` is ``None`` or does not start with ``RSRoute_``.
        InvalidMasterKey: When `master_key` does not match the configured ``RSRoute_MASTER_KEY``.
    """

    if master_key is None:
        raise AuthenticationError("Invalid `master_key`, `None`")
    
    if not(master_key.startswith("RSRoute_")):
        raise InvalidMasterKey("given master_key should start with `RSRoute_`.")
    
    # Will handle not start RSRoute_ & Empty Password both at once.
    if not(os.getenv("RSRoute_MASTER_KEY").startswith("RSRoute_")):
        raise InvalidMasterKey("Master Key is not started with `RSRoute_`, try to edit `.env`")
    
    if len(os.getenv("RSRoute_MASTER_KEY")) < 14:
        raise InvalidMasterKey("Master Key can't be smaller than 6. (14)")
    
    if master_key == os.getenv("RSRoute_MASTER_KEY"):
        return True # Able to Login.
    else:
        raise AuthenticationError("Invalid `master_key`. Input correct `master_key`")
    


