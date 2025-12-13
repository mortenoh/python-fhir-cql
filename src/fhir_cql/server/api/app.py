"""FastAPI application factory for FHIR server."""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config.settings import FHIRServerSettings
from ..generator import PatientRecordGenerator
from ..storage.fhir_store import FHIRStore
from .routes import create_router

logger = logging.getLogger(__name__)


def create_app(
    settings: FHIRServerSettings | None = None,
    store: FHIRStore | None = None,
) -> FastAPI:
    """Create and configure the FHIR server FastAPI application.

    Args:
        settings: Server settings (uses defaults if None)
        store: FHIR data store (creates new if None)

    Returns:
        Configured FastAPI application
    """
    if settings is None:
        settings = FHIRServerSettings()

    if store is None:
        store = FHIRStore()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan handler."""
        # Startup
        logger.info("Starting FHIR server...")

        # Generate synthetic data if requested
        if settings.patients > 0:
            logger.info(f"Generating {settings.patients} synthetic patients...")
            generator = PatientRecordGenerator(seed=settings.seed)
            resources = generator.generate_population(settings.patients)

            for resource in resources:
                store.create(resource)

            logger.info(f"Generated {len(resources)} resources for {settings.patients} patients")

        # Store references in app state
        app.state.store = store
        app.state.settings = settings

        yield

        # Shutdown
        logger.info("Shutting down FHIR server...")

    app = FastAPI(
        title=settings.server_name,
        description="FHIR R4 REST Server with synthetic data generation",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_docs else None,
    )

    # Add CORS middleware
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Create and include FHIR router
    base_url = f"http://{settings.host}:{settings.port}"
    fhir_router = create_router(store=store, base_url=base_url)
    app.include_router(fhir_router)

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root() -> dict[str, Any]:
        """Root endpoint with server information."""
        return {
            "name": settings.server_name,
            "fhirVersion": "4.0.1",
            "status": "running",
            "endpoints": {
                "metadata": "/metadata",
                "docs": "/docs" if settings.enable_docs else None,
            },
        }

    return app


def run_server(
    settings: FHIRServerSettings | None = None,
    store: FHIRStore | None = None,
) -> None:
    """Run the FHIR server with uvicorn.

    Args:
        settings: Server settings
        store: Optional pre-configured store
    """
    import uvicorn

    if settings is None:
        settings = FHIRServerSettings()

    app = create_app(settings=settings, store=store)

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
