"""DeviceMetric resource generator."""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class DeviceMetricGenerator(FHIRResourceGenerator):
    """Generator for FHIR DeviceMetric resources."""

    # Metric types (IEEE 11073 MDC)
    METRIC_TYPES = [
        {"code": "150456", "display": "SpO2", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150020", "display": "Heart Rate", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150021", "display": "Systolic Blood Pressure", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150022", "display": "Diastolic Blood Pressure", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150276", "display": "Respiratory Rate", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150364", "display": "Body Temperature", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "160252", "display": "Blood Glucose", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "150088", "display": "Mean Blood Pressure", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "151562", "display": "ECG Lead II", "system": "urn:iso:std:iso:11073:10101"},
        {"code": "153856", "display": "EtCO2", "system": "urn:iso:std:iso:11073:10101"},
    ]

    # Measurement units
    UNITS = [
        {"code": "%", "display": "Percent", "system": "http://unitsofmeasure.org"},
        {"code": "{Beats}/min", "display": "Beats per minute", "system": "http://unitsofmeasure.org"},
        {"code": "mm[Hg]", "display": "mmHg", "system": "http://unitsofmeasure.org"},
        {"code": "{Breaths}/min", "display": "Breaths per minute", "system": "http://unitsofmeasure.org"},
        {"code": "Cel", "display": "Celsius", "system": "http://unitsofmeasure.org"},
        {"code": "mg/dL", "display": "mg/dL", "system": "http://unitsofmeasure.org"},
        {"code": "mV", "display": "milliVolt", "system": "http://unitsofmeasure.org"},
    ]

    # Operational status
    OPERATIONAL_STATUS = ["on", "off", "standby", "entered-in-error"]

    # Categories
    CATEGORIES = ["measurement", "setting", "calculation", "unspecified"]

    # Colors
    COLORS = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

    # Calibration types
    CALIBRATION_TYPES = ["unspecified", "offset", "gain", "two-point"]

    # Calibration states
    CALIBRATION_STATES = ["not-calibrated", "calibration-required", "calibrated", "unspecified"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        metric_id: str | None = None,
        device_ref: str | None = None,
        parent_ref: str | None = None,
        metric_type: str | None = None,
        operational_status: str = "on",
        category: str = "measurement",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a DeviceMetric resource.

        Args:
            metric_id: Metric ID (generates UUID if None)
            device_ref: Reference to source Device
            parent_ref: Reference to parent DeviceMetric
            metric_type: IEEE 11073 metric type code (random if None)
            operational_status: Metric operational status
            category: Metric category

        Returns:
            DeviceMetric FHIR resource
        """
        if metric_id is None:
            metric_id = self._generate_id()

        # Select metric type
        if metric_type is None:
            type_coding = self.faker.random_element(self.METRIC_TYPES)
        else:
            type_coding = next(
                (t for t in self.METRIC_TYPES if t["code"] == metric_type),
                self.METRIC_TYPES[0],
            )

        # Select appropriate unit
        unit = self.faker.random_element(self.UNITS)
        color = self.faker.random_element(self.COLORS)

        metric: dict[str, Any] = {
            "resourceType": "DeviceMetric",
            "id": metric_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/device-metric-ids",
                    value=f"DM-{self.faker.numerify('########')}",
                ),
            ],
            "type": {
                "coding": [type_coding],
                "text": type_coding["display"],
            },
            "unit": {
                "coding": [unit],
                "text": unit["display"],
            },
            "operationalStatus": operational_status,
            "color": color,
            "category": category,
            "measurementPeriod": {
                "repeat": {
                    "frequency": 1,
                    "period": self.faker.random_element([1, 5, 10, 30, 60]),
                    "periodUnit": "s",
                }
            },
            "calibration": [
                {
                    "type": self.faker.random_element(self.CALIBRATION_TYPES),
                    "state": self.faker.random_element(self.CALIBRATION_STATES),
                    "time": self._generate_datetime(start_date=datetime.now(timezone.utc) - timedelta(days=30)),
                }
            ],
        }

        if device_ref:
            metric["source"] = {"reference": device_ref}

        if parent_ref:
            metric["parent"] = {"reference": parent_ref}

        return metric
