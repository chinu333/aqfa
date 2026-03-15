"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AzureQuantumConfig:
    """Azure Quantum workspace configuration (API key authentication)."""
    connection_string: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_CONNECTION_STRING", ""))
    api_key: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_API_KEY", ""))
    endpoint: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_ENDPOINT", ""))
    resource_id: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_RESOURCE_ID", ""))
    location: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_LOCATION", "eastus"))
    subscription_id: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_SUBSCRIPTION_ID", ""))
    resource_group: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_RESOURCE_GROUP", ""))
    workspace_name: str = field(default_factory=lambda: os.getenv("AZURE_QUANTUM_WORKSPACE_NAME", ""))
    target_sc: str = field(default_factory=lambda: os.getenv("QUANTINUUM_TARGET_SC", "quantinuum.sim.h2-1sc"))
    target_em: str = field(default_factory=lambda: os.getenv("QUANTINUUM_TARGET_EM", "quantinuum.sim.h2-1e"))


@dataclass
class AzureAuthConfig:
    """Azure authentication — API key is the primary method.
    Service-principal fields kept for future use if needed."""
    tenant_id: str = field(default_factory=lambda: os.getenv("AZURE_TENANT_ID", ""))
    client_id: str = field(default_factory=lambda: os.getenv("AZURE_CLIENT_ID", ""))
    client_secret: str = field(default_factory=lambda: os.getenv("AZURE_CLIENT_SECRET", ""))


@dataclass
class FlaskConfig:
    """Flask application configuration."""
    secret_key: str = field(default_factory=lambda: os.getenv("FLASK_SECRET_KEY", "dev-secret-key"))
    debug: bool = field(default_factory=lambda: os.getenv("FLASK_DEBUG", "0") == "1")
    host: str = field(default_factory=lambda: os.getenv("FLASK_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("FLASK_PORT", "5000")))


# --- Future service configs (uncomment when ready) ---

@dataclass
class AzureOpenAIConfig:
    """Azure OpenAI configuration (future)."""
    endpoint: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    api_key: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY", ""))
    deployment: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"))
    api_version: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"))


@dataclass
class AzureAISearchConfig:
    """Azure AI Search configuration (future)."""
    endpoint: str = field(default_factory=lambda: os.getenv("AZURE_SEARCH_ENDPOINT", ""))
    api_key: str = field(default_factory=lambda: os.getenv("AZURE_SEARCH_API_KEY", ""))
    index_name: str = field(default_factory=lambda: os.getenv("AZURE_SEARCH_INDEX", "qdk-chemistry-index"))


@dataclass
class AzureSpeechConfig:
    """Azure Speech configuration (future)."""
    key: str = field(default_factory=lambda: os.getenv("AZURE_SPEECH_KEY", ""))
    region: str = field(default_factory=lambda: os.getenv("AZURE_SPEECH_REGION", "eastus"))


@dataclass
class AzureDocIntelConfig:
    """Azure Document Intelligence configuration (future)."""
    endpoint: str = field(default_factory=lambda: os.getenv("AZURE_DOC_INTEL_ENDPOINT", ""))
    key: str = field(default_factory=lambda: os.getenv("AZURE_DOC_INTEL_KEY", ""))


@dataclass
class AppConfig:
    """Master application configuration aggregating all service configs."""
    flask: FlaskConfig = field(default_factory=FlaskConfig)
    quantum: AzureQuantumConfig = field(default_factory=AzureQuantumConfig)
    auth: AzureAuthConfig = field(default_factory=AzureAuthConfig)
    openai: AzureOpenAIConfig = field(default_factory=AzureOpenAIConfig)
    ai_search: AzureAISearchConfig = field(default_factory=AzureAISearchConfig)
    speech: AzureSpeechConfig = field(default_factory=AzureSpeechConfig)
    doc_intel: AzureDocIntelConfig = field(default_factory=AzureDocIntelConfig)

    @property
    def is_quantum_configured(self) -> bool:
        return bool(self.quantum.connection_string or self.quantum.resource_id)

    @property
    def is_openai_configured(self) -> bool:
        return bool(self.openai.endpoint and self.openai.api_key)

    @property
    def is_search_configured(self) -> bool:
        return bool(self.ai_search.endpoint and self.ai_search.api_key)

    @property
    def is_speech_configured(self) -> bool:
        return bool(self.speech.key)

    @property
    def is_doc_intel_configured(self) -> bool:
        return bool(self.doc_intel.endpoint and self.doc_intel.key)
