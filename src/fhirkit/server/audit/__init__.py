"""Audit logging service for FHIR operations.

This module provides automatic audit logging for all FHIR CRUD operations,
creating AuditEvent resources that comply with the FHIR R4 specification.

Usage:
    from fhirkit.server.audit import AuditService

    audit_service = AuditService(store, enabled=True)
    audit_service.log_create(request, resource, outcome="0")
"""

from .service import AuditAction, AuditOutcome, AuditService

__all__ = [
    "AuditService",
    "AuditAction",
    "AuditOutcome",
]
