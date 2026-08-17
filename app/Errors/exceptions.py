# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"BaseErrors for RSRoute"

class RSRouteError(Exception):
    """Base exception for all RSRoute exceptions."""

    pass


class AuthenticationError(RSRouteError):
    """Raised when authentication fails."""

    pass


class InvalidMasterKey(RSRouteError):
    """Raised when the master key format is invalid."""

    pass


class UnsupportedProvider(RSRouteError):
    """Raised when an unsupported provider is requested."""

    pass


class ProviderNotConfigured(RSRouteError):
    """Raised when a provider is not configured."""

    pass


class InvalidRequest(RSRouteError):
    """Raised when a request is invalid."""

    pass


class ProviderConnectionError(RSRouteError):
    """Raised when a provider cannot be reached."""

    pass


class GenerationError(RSRouteError):
    """Raised when text generation fails."""

    pass


if __name__ == "__main__":
    raise UnsupportedProvider("Groq Not Supported")