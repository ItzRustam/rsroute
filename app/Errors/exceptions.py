# rsllm
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"BaseErrors for rsllm"

class RSLLMError(Exception):
    """Base exception for all rsllm exceptions."""

    pass


class AuthenticationError(RSLLMError):
    """Raised when authentication fails."""

    pass


class InvalidMasterKey(RSLLMError):
    """Raised when the master key format is invalid."""

    pass


class UnsupportedProvider(RSLLMError):
    """Raised when an unsupported provider is requested."""

    pass


class ProviderNotConfigured(RSLLMError):
    """Raised when a provider is not configured."""

    pass


class InvalidRequest(RSLLMError):
    """Raised when a request is invalid."""

    pass


class ProviderConnectionError(RSLLMError):
    """Raised when a provider cannot be reached."""

    pass


class GenerationError(RSLLMError):
    """Raised when text generation fails."""

    pass


if __name__ == "__main__":
    raise UnsupportedProvider("Groq Not Supported")