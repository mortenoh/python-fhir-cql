"""FHIR Server configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings


class FHIRServerSettings(BaseSettings):
    """Application settings for FHIR Server."""

    # Server info
    server_name: str = "FHIR R4 Server"
    host: str = "0.0.0.0"
    port: int = 8080
    base_path: str = ""

    # Data generation
    patients: int = Field(
        default=0,
        description="Number of synthetic patients to generate on startup",
    )
    seed: int | None = Field(
        default=None,
        description="Random seed for reproducible data generation",
    )

    # Preload paths
    preload_cql: str | None = Field(
        default=None,
        description="Directory containing CQL libraries to preload",
    )
    preload_valuesets: str | None = Field(
        default=None,
        description="Directory containing ValueSet JSON files to preload",
    )
    preload_data: str | None = Field(
        default=None,
        description="Path to FHIR Bundle or ndjson file to preload",
    )

    # Terminology
    enable_terminology: bool = Field(
        default=True,
        description="Enable terminology operations ($validate-code, $expand, etc.)",
    )

    # API documentation
    enable_docs: bool = Field(
        default=True,
        description="Enable Swagger/OpenAPI documentation endpoints",
    )

    # Security
    enable_cors: bool = True
    cors_origins: list[str] = Field(default=["*"])

    # Logging
    log_level: str = "INFO"
    log_requests: bool = True

    # Limits
    default_page_size: int = 100
    max_page_size: int = 1000

    model_config = {
        "env_prefix": "FHIR_SERVER_",
        "env_file": ".env",
        "extra": "ignore",
    }
