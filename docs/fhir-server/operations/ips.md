# International Patient Summary (IPS)

FHIRKit implements the **IPS $summary operation** per the [HL7 IPS Implementation Guide](http://hl7.org/fhir/uv/ips/).

## What is IPS?

The International Patient Summary is a standardized FHIR document containing essential patient health information for cross-border and cross-organization care. It provides a "minimal viable dataset" that any clinician can understand.

## IPS Sections

An IPS document includes these sections:

| Section | LOINC Code | Resource Type |
|---------|------------|---------------|
| Allergies and Intolerances | 48765-2 | AllergyIntolerance |
| Medication Summary | 10160-0 | MedicationRequest |
| Active Problems | 11450-4 | Condition |
| Immunizations | 11369-6 | Immunization |
| History of Procedures | 47519-4 | Procedure |
| Results | 30954-2 | Observation (laboratory) |
| Vital Signs | 8716-3 | Observation (vital-signs) |

## Generate IPS

### API

```http
GET /baseR4/Patient/{id}/$summary
```

**Parameters:**
- `persist` (optional, default: false) - Whether to save the generated Bundle

**Response:** Document Bundle containing IPS Composition and all referenced resources

### Example

```bash
# Generate IPS for patient
curl http://localhost:8080/baseR4/Patient/12345/$summary

# Generate and persist
curl "http://localhost:8080/baseR4/Patient/12345/$summary?persist=true"
```

### Python

```python
import httpx

# Generate IPS
response = httpx.get("http://localhost:8080/baseR4/Patient/12345/$summary")
ips_bundle = response.json()

# Access sections
composition = ips_bundle["entry"][0]["resource"]
for section in composition["section"]:
    print(f"{section['title']}: {len(section.get('entry', []))} items")
```

## Import IPS

Accept an IPS document and import resources into the server.

### API

```http
POST /baseR4/Patient/$summary
Content-Type: application/fhir+json

{IPS Document Bundle}
```

**Response:** OperationOutcome with import summary

### Example

```bash
# Import IPS from file
curl -X POST http://localhost:8080/baseR4/Patient/\$summary \
  -H "Content-Type: application/fhir+json" \
  -d @ips-document.json
```

## Web UI

Access the IPS generator at `/ips`:

- **Generate**: Select a patient and click "Generate IPS"
- **View**: Rendered view with collapsible sections
- **Download**: Export as JSON file
- **Import**: Upload an IPS document

## IPS Document Structure

```
Bundle (type: document)
├── Composition (IPS)
│   ├── subject → Patient
│   ├── section[allergies] → AllergyIntolerance[]
│   ├── section[medications] → MedicationRequest[]
│   ├── section[problems] → Condition[]
│   ├── section[immunizations] → Immunization[]
│   ├── section[procedures] → Procedure[]
│   ├── section[results] → Observation[]
│   └── section[vital_signs] → Observation[]
├── Patient
├── AllergyIntolerance[]
├── MedicationRequest[]
├── Condition[]
├── Immunization[]
├── Procedure[]
└── Observation[]
```

## Profile Compliance

Generated IPS documents conform to:
- Bundle: `http://hl7.org/fhir/uv/ips/StructureDefinition/Bundle-uv-ips`
- Composition: `http://hl7.org/fhir/uv/ips/StructureDefinition/Composition-uv-ips`

## Use Cases

1. **Patient Transfer**: Generate IPS when transferring patient to another facility
2. **Emergency Access**: Quick summary for emergency department
3. **Cross-Border Care**: Portable summary for international patients
4. **Patient Portal**: Allow patients to download their health summary
5. **Data Exchange**: Share standardized patient data between systems

## Related

- [Patient $everything](../resources/patient.md) - All patient resources (not document format)
- [Composition $document](../resources/composition.md) - Generic document generation
- [HL7 IPS IG](http://hl7.org/fhir/uv/ips/) - Official specification
