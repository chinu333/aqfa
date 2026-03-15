"""Base service class — all Azure service integrations inherit from this."""

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base for pluggable Azure service integrations.

    Extend this class when adding new Azure services (OpenAI, Speech, etc.).
    The service registry in the Flask app will auto-discover subclasses.
    """

    def __init__(self, config: Any):
        self._config = config
        self._initialized = False

    @property
    def name(self) -> str:
        """Human-readable service name."""
        return self.__class__.__name__

    @property
    def is_configured(self) -> bool:
        """Whether required config values are present."""
        return False

    @abstractmethod
    def initialize(self) -> None:
        """Connect / authenticate to the backing Azure resource."""
        ...

    @abstractmethod
    def health_check(self) -> dict:
        """Return service health status."""
        ...

    def to_status_dict(self) -> dict:
        return {
            "service": self.name,
            "configured": self.is_configured,
            "initialized": self._initialized,
        }
