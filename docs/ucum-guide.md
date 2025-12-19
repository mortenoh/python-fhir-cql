# UCUM Unit Conversion Guide

This guide covers the UCUM (Unified Code for Units of Measure) support in FHIRKit for converting clinical measurements between different units.

## Overview

UCUM is a code system for unambiguous representation of measurement units. FHIRKit implements a subset of UCUM commonly used in clinical settings, enabling:

- Drug dosage calculations
- Patient measurement conversions (weight, height, temperature)
- Lab value unit conversions
- IV fluid calculations

## Quick Start

### CQL Expression

```cql
// Convert 150 pounds to kilograms
define WeightInKg: ConvertQuantity(150 '[lb_av]', 'kg')
// Result: 68.04 'kg'

// Convert body temperature
define TempCelsius: ConvertQuantity(98.6 '[degF]', 'Cel')
// Result: 37.0 'Cel'
```

### Python API

```python
from fhirkit.engine.units import convert_quantity

# Basic conversion
result = convert_quantity(1, "g", "mg")  # 1000.0

# Temperature
temp_c = convert_quantity(98.6, "[degF]", "Cel")  # 37.0

# Weight
weight_kg = convert_quantity(150, "[lb_av]", "kg")  # 68.04
```

### Server API

```bash
curl -X POST http://localhost:8000/$cql \
  -H "Content-Type: application/json" \
  -d '{"code": "define Weight: ConvertQuantity(150 '\''[lb_av]'\'', '\''kg'\'')"}'
```

## Supported Units

### Mass Units

| UCUM Code | Name | Metric |
|-----------|------|--------|
| `g` | gram | Yes |
| `mg` | milligram | Yes |
| `kg` | kilogram | Yes |
| `ug` | microgram | Yes |
| `ng` | nanogram | Yes |
| `[lb_av]` | pound (avoirdupois) | No |
| `[oz_av]` | ounce (avoirdupois) | No |
| `[gr]` | grain | No |
| `[stone_av]` | stone | No |

**Examples:**
```cql
ConvertQuantity(1 'g', 'mg')           // 1000 'mg'
ConvertQuantity(500 'mg', 'g')         // 0.5 'g'
ConvertQuantity(1 'kg', 'g')           // 1000 'g'
ConvertQuantity(150 '[lb_av]', 'kg')   // 68.04 'kg'
ConvertQuantity(1 'kg', '[lb_av]')     // 2.205 '[lb_av]'
```

### Volume Units

| UCUM Code | Name | Metric |
|-----------|------|--------|
| `L` | liter | Yes |
| `mL` | milliliter | Yes |
| `dL` | deciliter | Yes |
| `uL` | microliter | Yes |
| `[gal_us]` | US gallon | No |
| `[qt_us]` | US quart | No |
| `[pt_us]` | US pint | No |
| `[foz_us]` | US fluid ounce | No |
| `[cup_us]` | US cup | No |
| `[tbs_us]` | US tablespoon | No |
| `[tsp_us]` | US teaspoon | No |

**Examples:**
```cql
ConvertQuantity(1 'L', 'mL')           // 1000 'mL'
ConvertQuantity(500 'mL', 'L')         // 0.5 'L'
ConvertQuantity(1 'L', 'dL')           // 10 'dL'
ConvertQuantity(1 '[gal_us]', 'L')     // 3.785 'L'
```

### Length Units

| UCUM Code | Name | Metric |
|-----------|------|--------|
| `m` | meter | Yes |
| `cm` | centimeter | Yes |
| `mm` | millimeter | Yes |
| `km` | kilometer | Yes |
| `[in_i]` | inch (international) | No |
| `[ft_i]` | foot (international) | No |
| `[yd_i]` | yard (international) | No |
| `[mi_i]` | mile (international) | No |

**Examples:**
```cql
ConvertQuantity(1 'm', 'cm')           // 100 'cm'
ConvertQuantity(100 'cm', 'm')         // 1 'm'
ConvertQuantity(70 '[in_i]', 'cm')     // 177.8 'cm'
ConvertQuantity(6 '[ft_i]', 'm')       // 1.8288 'm'
```

### Temperature Units

| UCUM Code | Name |
|-----------|------|
| `K` | Kelvin (base unit) |
| `Cel` | Celsius |
| `[degF]` | Fahrenheit |

**Examples:**
```cql
// Body temperature
ConvertQuantity(98.6 '[degF]', 'Cel')  // 37.0 'Cel'
ConvertQuantity(37 'Cel', '[degF]')    // 98.6 '[degF]'

// Boiling/freezing points
ConvertQuantity(100 'Cel', '[degF]')   // 212 '[degF]'
ConvertQuantity(0 'Cel', 'K')          // 273.15 'K'
ConvertQuantity(32 '[degF]', 'Cel')    // 0 'Cel'
```

### Time Units

| UCUM Code | Name | Metric |
|-----------|------|--------|
| `s` | second | Yes |
| `min` | minute | No |
| `h` | hour | No |
| `d` | day | No |
| `wk` | week | No |
| `mo` | month (average) | No |
| `a` | year (Julian) | No |

**Examples:**
```cql
ConvertQuantity(1 'min', 's')          // 60 's'
ConvertQuantity(1 'h', 'min')          // 60 'min'
ConvertQuantity(1 'd', 'h')            // 24 'h'
ConvertQuantity(1 'wk', 'd')           // 7 'd'
```

### Concentration Units (Compound)

Compound units combine base units with division:

| Example | Description |
|---------|-------------|
| `mg/dL` | milligrams per deciliter |
| `mg/L` | milligrams per liter |
| `g/L` | grams per liter |
| `mmol/L` | millimoles per liter |
| `mEq/L` | milliequivalents per liter |
| `mg/mL` | milligrams per milliliter |

**Examples:**
```cql
// Glucose conversion
ConvertQuantity(180 'mg/dL', 'mg/L')   // 1800 'mg/L'
ConvertQuantity(1 'g/L', 'mg/dL')      // 100 'mg/dL'

// Drug concentration
ConvertQuantity(50 'mg/mL', 'g/L')     // 50 'g/L'
```

### Clinical Special Units

| UCUM Code | Name |
|-----------|------|
| `[IU]` | International Unit |
| `[arb'U]` | Arbitrary Unit |
| `%` | Percent |
| `mm[Hg]` | Millimeters of mercury (pressure) |
| `[psi]` | Pounds per square inch |
| `[pH]` | pH |

## Common Clinical Conversions

### Patient Measurements

```cql
// Weight: US to Metric
define WeightKg: ConvertQuantity(PatientWeightLbs '[lb_av]', 'kg')

// Height: US to Metric
define HeightCm: ConvertQuantity(PatientHeightInches '[in_i]', 'cm')

// Temperature: US to Metric
define TempCelsius: ConvertQuantity(PatientTempF '[degF]', 'Cel')
```

### Medication Dosing

```cql
// Convert dose to different units
define DoseInGrams: ConvertQuantity(500 'mg', 'g')
// Result: 0.5 'g'

// Drug concentration
define Concentration: ConvertQuantity(250 'mg/mL', 'g/L')
// Result: 250 'g/L'
```

### Lab Values

```cql
// Glucose conversion (note: this is unit conversion only)
// For molar conversion, you need molecular weight
define GlucoseMgL: ConvertQuantity(180 'mg/dL', 'mg/L')
// Result: 1800 'mg/L'
```

### IV Fluid Calculations

```cql
// Convert flow rate
define FlowRateLitersPerHour: ConvertQuantity(125 'mL/h', 'L/h')
// Result: 0.125 'L/h'

// Total volume
define TotalVolumeLiters: ConvertQuantity(1000 'mL', 'L')
// Result: 1 'L'
```

## Unit Aliases

For convenience, FHIRKit accepts common aliases:

| Alias | UCUM Code |
|-------|-----------|
| `mcg` | `ug` (microgram) |
| `sec` | `s` (second) |
| `hr` | `h` (hour) |
| `yr` | `a` (year) |
| `cc` | `mL` (cubic centimeter) |
| `lbs`, `lb` | `[lb_av]` (pound) |
| `oz` | `[oz_av]` (ounce) |
| `in` | `[in_i]` (inch) |
| `ft` | `[ft_i]` (foot) |
| `mi` | `[mi_i]` (mile) |
| `gal` | `[gal_us]` (gallon) |
| `degC`, `celsius` | `Cel` |
| `degF`, `fahrenheit` | `[degF]` |

## Python API Reference

### convert_quantity()

```python
from fhirkit.engine.units import convert_quantity

result = convert_quantity(value, from_unit, to_unit)
```

**Parameters:**
- `value`: Numeric value to convert (float, Decimal, or Quantity)
- `from_unit`: Source unit (UCUM code)
- `to_unit`: Target unit (UCUM code)

**Returns:** Converted value as float, or None if conversion fails

**Example:**
```python
from fhirkit.engine.units import convert_quantity

# Basic
convert_quantity(1, "g", "mg")  # 1000.0

# With Decimal precision
from decimal import Decimal
convert_quantity(Decimal("1.5"), "kg", "g")  # 1500.0

# Temperature (special handling)
convert_quantity(98.6, "[degF]", "Cel")  # 37.0
```

### parse_unit()

```python
from fhirkit.engine.units import parse_unit

parsed = parse_unit("mg/dL")
print(parsed.dimension)  # Dimension info
print(parsed.factor)     # Conversion factor
```

### UCUMConverter class

```python
from fhirkit.engine.units import UCUMConverter

converter = UCUMConverter()

# Parse a unit
parsed = converter.parse("mg")

# Convert
result = converter.convert(100, "mg", "g")  # 0.1

# Check compatibility
if converter.is_compatible("g", "mg"):
    print("Units are compatible")
```

## Error Handling

```python
from fhirkit.engine.units.ucum import (
    UCUMError,
    UnitParseError,
    IncompatibleUnitsError,
)

try:
    result = convert_quantity(1, "invalid_unit", "g")
except UnitParseError as e:
    print(f"Cannot parse unit: {e}")

try:
    result = convert_quantity(1, "g", "L")  # mass vs volume
except IncompatibleUnitsError as e:
    print(f"Incompatible units: {e}")
```

## Limitations

1. **No molar conversions**: Converting between mass and molar units (e.g., mg/dL to mmol/L for glucose) requires molecular weight, which is substance-specific. UCUM handles unit dimensions only.

2. **Precision**: Results are returned as Python floats. For high-precision calculations, use Decimal inputs.

3. **Subset implementation**: This implements common clinical units. Specialized units may not be available.

4. **No unit inference**: You must provide explicit units; the system doesn't infer units from context.

## References

- [UCUM Specification](https://ucum.org/ucum)
- [UCUM Essence](https://ucum.org/ucum-essence.xml)
- [HL7 FHIR Quantity](https://hl7.org/fhir/datatypes.html#Quantity)
