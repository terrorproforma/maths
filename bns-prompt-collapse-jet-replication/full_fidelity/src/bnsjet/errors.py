"""Project-specific exceptions."""

from __future__ import annotations


class BNSJetError(RuntimeError):
    """Base error for the replication tooling."""


class ConfigurationError(BNSJetError):
    """Raised when a campaign or target document is invalid."""


class ArtifactError(BNSJetError):
    """Raised when a declared artifact is absent or has the wrong digest."""


class ValidationFailure(BNSJetError):
    """Raised when one or more blocking scientific validation targets fail."""
