"""Audit service for automatic FHIR operation logging.

Creates AuditEvent resources for CRUD operations following the
FHIR R4 AuditEvent specification.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastapi import Request

    from ..storage.fhir_store import FHIRStore

logger = logging.getLogger(__name__)


class AuditAction(str, Enum):
    """FHIR AuditEvent action codes."""

    CREATE = "C"
    READ = "R"
    UPDATE = "U"
    DELETE = "D"
    EXECUTE = "E"


class AuditOutcome(str, Enum):
    """FHIR AuditEvent outcome codes."""

    SUCCESS = "0"
    MINOR_FAILURE = "4"
    SERIOUS_FAILURE = "8"
    MAJOR_FAILURE = "12"


# FHIR RESTful interaction subtypes
REST_SUBTYPES: dict[str, dict[str, str]] = {
    "create": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "create",
        "display": "create",
    },
    "read": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "read",
        "display": "read",
    },
    "vread": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "vread",
        "display": "vread",
    },
    "update": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "update",
        "display": "update",
    },
    "delete": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "delete",
        "display": "delete",
    },
    "search": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "search-type",
        "display": "search",
    },
    "history": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "history-instance",
        "display": "history",
    },
    "batch": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "batch",
        "display": "batch",
    },
    "transaction": {
        "system": "http://hl7.org/fhir/restful-interaction",
        "code": "transaction",
        "display": "transaction",
    },
}


class AuditService:
    """Service for creating AuditEvent resources for FHIR operations.

    This service automatically logs CRUD operations as AuditEvent resources,
    providing a complete audit trail for compliance and security monitoring.
    """

    def __init__(
        self,
        store: FHIRStore,
        enabled: bool = True,
        exclude_reads: bool = True,
    ):
        """Initialize the audit service.

        Args:
            store: FHIR store for persisting AuditEvent resources
            enabled: Whether audit logging is enabled
            exclude_reads: Whether to exclude read operations from audit log
        """
        self.store = store
        self.enabled = enabled
        self.exclude_reads = exclude_reads

    def log_operation(
        self,
        request: Request,
        action: AuditAction,
        subtype: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
        resource: dict[str, Any] | None = None,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
        patient_ref: str | None = None,
    ) -> dict[str, Any] | None:
        """Log a FHIR operation as an AuditEvent.

        Args:
            request: FastAPI request object
            action: The action code (C, R, U, D, E)
            subtype: The REST interaction type (create, read, update, etc.)
            resource_type: Type of resource being accessed
            resource_id: ID of resource being accessed
            resource: The actual resource (for extracting patient reference)
            outcome: Outcome code (0=success, 4/8/12=failure)
            outcome_desc: Description of outcome for failures
            patient_ref: Explicit patient reference (overrides extraction)

        Returns:
            Created AuditEvent resource, or None if logging is disabled
        """
        if not self.enabled:
            return None

        if self.exclude_reads and action == AuditAction.READ:
            return None

        # Don't audit AuditEvent operations (prevent infinite loops)
        if resource_type == "AuditEvent":
            return None

        try:
            audit_event = self._create_audit_event(
                request=request,
                action=action,
                subtype=subtype,
                resource_type=resource_type,
                resource_id=resource_id,
                resource=resource,
                outcome=outcome,
                outcome_desc=outcome_desc,
                patient_ref=patient_ref,
            )

            # Create the AuditEvent (without triggering another audit)
            created = self.store.create(audit_event)
            logger.debug(f"Audit: {subtype} {resource_type}/{resource_id} -> {outcome}")
            return created

        except Exception as e:
            # Audit failures should not break the main operation
            logger.warning(f"Failed to create audit event: {e}")
            return None

    def _create_audit_event(
        self,
        request: Request,
        action: AuditAction,
        subtype: str,
        resource_type: str | None,
        resource_id: str | None,
        resource: dict[str, Any] | None,
        outcome: AuditOutcome,
        outcome_desc: str | None,
        patient_ref: str | None,
    ) -> dict[str, Any]:
        """Create an AuditEvent resource.

        Returns:
            AuditEvent FHIR resource dictionary
        """
        now = datetime.now(timezone.utc)

        audit_event: dict[str, Any] = {
            "resourceType": "AuditEvent",
            "id": str(uuid.uuid4()),
            "meta": {
                "versionId": "1",
                "lastUpdated": now.isoformat(),
            },
            "type": {
                "system": "http://terminology.hl7.org/CodeSystem/audit-event-type",
                "code": "rest",
                "display": "RESTful Operation",
            },
            "subtype": [REST_SUBTYPES.get(subtype, REST_SUBTYPES["read"])],
            "action": action.value,
            "recorded": now.isoformat(),
            "outcome": outcome.value,
        }

        # Add outcome description for failures
        if outcome != AuditOutcome.SUCCESS and outcome_desc:
            audit_event["outcomeDesc"] = outcome_desc

        # Add agent (who performed the action)
        agent = self._create_agent(request)
        audit_event["agent"] = [agent]

        # Add source (the server)
        audit_event["source"] = {
            "observer": {"display": "FHIR Server"},
            "type": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/security-source-type",
                    "code": "4",
                    "display": "Application Server",
                }
            ],
        }

        # Add entity (what was accessed)
        entities: list[dict[str, Any]] = []

        # Extract patient reference from resource if available
        if not patient_ref and resource:
            patient_ref = self._extract_patient_reference(resource)

        if patient_ref:
            entities.append(
                {
                    "what": {"reference": patient_ref},
                    "type": {
                        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
                        "code": "1",
                        "display": "Person",
                    },
                    "role": {
                        "system": "http://terminology.hl7.org/CodeSystem/object-role",
                        "code": "1",
                        "display": "Patient",
                    },
                }
            )

        if resource_type and resource_id:
            entities.append(
                {
                    "what": {"reference": f"{resource_type}/{resource_id}"},
                    "type": {
                        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
                        "code": "2",
                        "display": "System Object",
                    },
                    "name": resource_type,
                }
            )
        elif resource_type:
            entities.append(
                {
                    "what": {"display": f"{resource_type} search"},
                    "type": {
                        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
                        "code": "2",
                        "display": "System Object",
                    },
                    "name": resource_type,
                }
            )

        # Add query string for search operations
        if subtype == "search" and request.url.query:
            if entities:
                entities[-1]["query"] = request.url.query

        if entities:
            audit_event["entity"] = entities

        return audit_event

    def _create_agent(self, request: Request) -> dict[str, Any]:
        """Create the agent element from request information.

        Returns:
            Agent dictionary for AuditEvent
        """
        agent: dict[str, Any] = {
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                        "code": "IRCP",
                        "display": "information recipient",
                    }
                ]
            },
            "requestor": True,
        }

        # Try to get client IP
        client_ip = None
        if request.client:
            client_ip = request.client.host

        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()

        if client_ip:
            agent["network"] = {
                "address": client_ip,
                "type": "2",  # IP Address
            }

        # Add user agent as display
        user_agent = request.headers.get("User-Agent", "Unknown")
        agent["who"] = {"display": user_agent[:100]}  # Truncate long user agents

        return agent

    def _extract_patient_reference(self, resource: dict[str, Any]) -> str | None:
        """Extract patient reference from a resource.

        Checks common fields where patient references appear.

        Returns:
            Patient reference string (e.g., "Patient/123") or None
        """
        resource_type = resource.get("resourceType", "")

        # Direct patient reference
        if resource_type == "Patient":
            resource_id = resource.get("id")
            if resource_id:
                return f"Patient/{resource_id}"

        # Common patient reference fields
        patient_fields = [
            "patient",
            "subject",
            "individual",
            "beneficiary",
            "for",
        ]

        for field in patient_fields:
            ref = resource.get(field)
            if isinstance(ref, dict):
                reference = ref.get("reference", "")
                if reference.startswith("Patient/"):
                    return reference

        return None

    # Convenience methods for common operations

    def log_create(
        self,
        request: Request,
        resource: dict[str, Any],
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
    ) -> dict[str, Any] | None:
        """Log a create operation."""
        return self.log_operation(
            request=request,
            action=AuditAction.CREATE,
            subtype="create",
            resource_type=resource.get("resourceType"),
            resource_id=resource.get("id"),
            resource=resource,
            outcome=outcome,
            outcome_desc=outcome_desc,
        )

    def log_read(
        self,
        request: Request,
        resource_type: str,
        resource_id: str,
        resource: dict[str, Any] | None = None,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
    ) -> dict[str, Any] | None:
        """Log a read operation."""
        return self.log_operation(
            request=request,
            action=AuditAction.READ,
            subtype="read",
            resource_type=resource_type,
            resource_id=resource_id,
            resource=resource,
            outcome=outcome,
            outcome_desc=outcome_desc,
        )

    def log_update(
        self,
        request: Request,
        resource: dict[str, Any],
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
    ) -> dict[str, Any] | None:
        """Log an update operation."""
        return self.log_operation(
            request=request,
            action=AuditAction.UPDATE,
            subtype="update",
            resource_type=resource.get("resourceType"),
            resource_id=resource.get("id"),
            resource=resource,
            outcome=outcome,
            outcome_desc=outcome_desc,
        )

    def log_delete(
        self,
        request: Request,
        resource_type: str,
        resource_id: str,
        resource: dict[str, Any] | None = None,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
    ) -> dict[str, Any] | None:
        """Log a delete operation."""
        return self.log_operation(
            request=request,
            action=AuditAction.DELETE,
            subtype="delete",
            resource_type=resource_type,
            resource_id=resource_id,
            resource=resource,
            outcome=outcome,
            outcome_desc=outcome_desc,
        )

    def log_search(
        self,
        request: Request,
        resource_type: str,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        outcome_desc: str | None = None,
    ) -> dict[str, Any] | None:
        """Log a search operation."""
        return self.log_operation(
            request=request,
            action=AuditAction.READ,
            subtype="search",
            resource_type=resource_type,
            outcome=outcome,
            outcome_desc=outcome_desc,
        )
