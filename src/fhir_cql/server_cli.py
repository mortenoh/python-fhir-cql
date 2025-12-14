"""FHIR Server CLI commands."""

import json
from pathlib import Path

import typer
from rich import print as rprint
from rich.table import Table

app = typer.Typer(
    name="server",
    help="FHIR R4 server utilities (generate, load, stats, info). Use 'fhir serve' to start the server.",
    no_args_is_help=True,
)


@app.command("generate")
def generate(
    output: Path = typer.Argument(..., help="Output JSON file path"),
    patients: int = typer.Option(10, "--patients", "-n", help="Number of patients to generate"),
    seed: int = typer.Option(None, "--seed", "-s", help="Random seed for reproducible data"),
    format: str = typer.Option("bundle", "--format", "-f", help="Output format: bundle, ndjson, or files"),
    pretty: bool = typer.Option(True, "--pretty/--no-pretty", help="Pretty-print JSON output"),
) -> None:
    """Generate synthetic FHIR data to a file.

    Examples:
        # Generate 100 patients as a bundle
        fhir server generate ./data.json --patients 100

        # Generate with reproducible seed
        fhir server generate ./data.json --patients 50 --seed 42

        # Generate as NDJSON (one resource per line)
        fhir server generate ./data.ndjson --patients 100 --format ndjson
    """
    import uuid

    from fhir_cql.server.generator import PatientRecordGenerator

    rprint(f"[bold]Generating {patients} patient(s)...[/bold]")
    if seed:
        rprint(f"  Random seed: {seed}")

    generator = PatientRecordGenerator(seed=seed)
    resources = generator.generate_population(patients)

    rprint(f"  Generated {len(resources)} total resources")

    # Count by type
    by_type: dict[str, int] = {}
    for r in resources:
        rt = r.get("resourceType", "Unknown")
        by_type[rt] = by_type.get(rt, 0) + 1

    table = Table(title="Generated Resources")
    table.add_column("Resource Type", style="cyan")
    table.add_column("Count", justify="right")
    for rt, count in sorted(by_type.items()):
        table.add_row(rt, str(count))
    rprint(table)

    # Write output
    if format == "bundle":
        bundle = {
            "resourceType": "Bundle",
            "id": str(uuid.uuid4()),
            "type": "collection",
            "total": len(resources),
            "entry": [{"fullUrl": f"urn:uuid:{r.get('id', uuid.uuid4())}", "resource": r} for r in resources],
        }
        with open(output, "w") as f:
            json.dump(bundle, f, indent=2 if pretty else None)
        rprint(f"[green]Written to {output}[/green] (Bundle format)")

    elif format == "ndjson":
        with open(output, "w") as f:
            for r in resources:
                f.write(json.dumps(r) + "\n")
        rprint(f"[green]Written to {output}[/green] (NDJSON format)")

    elif format == "files":
        # Create directory structure
        output_dir = output.parent / output.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        for r in resources:
            rt = r.get("resourceType", "Unknown")
            rid = r.get("id", str(uuid.uuid4()))
            type_dir = output_dir / rt
            type_dir.mkdir(exist_ok=True)
            file_path = type_dir / f"{rid}.json"
            with open(file_path, "w") as f:
                json.dump(r, f, indent=2 if pretty else None)

        rprint(f"[green]Written to {output_dir}/[/green] (individual files)")

    else:
        rprint(f"[red]Unknown format: {format}[/red]")
        raise typer.Exit(1)


@app.command("load")
def load(
    input_file: Path = typer.Argument(..., help="FHIR JSON file to load (Bundle or single resource)"),
    url: str = typer.Option("http://localhost:8080", "--url", "-u", help="FHIR server base URL"),
    batch: bool = typer.Option(True, "--batch/--no-batch", help="Use batch transaction for loading"),
) -> None:
    """Load FHIR resources from a file into a running server.

    Examples:
        # Load a bundle into the server
        fhir server load ./data.json

        # Load to a specific server
        fhir server load ./data.json --url http://fhir.example.com

        # Load resources individually (no batch)
        fhir server load ./data.json --no-batch
    """
    import uuid

    import httpx

    if not input_file.exists():
        rprint(f"[red]Error:[/red] File not found: {input_file}")
        raise typer.Exit(1)

    # Load the file
    with open(input_file) as f:
        data = json.load(f)

    # Extract resources
    resources: list[dict] = []
    if data.get("resourceType") == "Bundle":
        for entry in data.get("entry", []):
            if "resource" in entry:
                resources.append(entry["resource"])
    else:
        resources.append(data)

    rprint(f"[bold]Loading {len(resources)} resource(s) to {url}[/bold]")

    if batch and len(resources) > 1:
        # Create batch bundle
        batch_bundle = {
            "resourceType": "Bundle",
            "id": str(uuid.uuid4()),
            "type": "batch",
            "entry": [
                {
                    "resource": r,
                    "request": {
                        "method": "POST",
                        "url": r.get("resourceType", ""),
                    },
                }
                for r in resources
            ],
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    url,
                    json=batch_bundle,
                    headers={"Content-Type": "application/fhir+json"},
                )

            if response.status_code in (200, 201):
                result = response.json()
                success = sum(
                    1 for e in result.get("entry", []) if e.get("response", {}).get("status", "").startswith("20")
                )
                rprint(f"[green]Batch complete:[/green] {success}/{len(resources)} resources created")
            else:
                rprint(f"[red]Batch failed:[/red] {response.status_code}")
                rprint(response.text[:500])
                raise typer.Exit(1)

        except httpx.RequestError as e:
            rprint(f"[red]Connection error:[/red] {e}")
            raise typer.Exit(1)

    else:
        # Load individually
        success = 0
        errors = 0

        with httpx.Client(timeout=30.0) as client:
            for r in resources:
                resource_type = r.get("resourceType")
                if not resource_type:
                    errors += 1
                    continue

                try:
                    response = client.post(
                        f"{url}/{resource_type}",
                        json=r,
                        headers={"Content-Type": "application/fhir+json"},
                    )

                    if response.status_code in (200, 201):
                        success += 1
                    else:
                        errors += 1
                        rprint(f"[yellow]Failed {resource_type}:[/yellow] {response.status_code}")

                except httpx.RequestError as e:
                    errors += 1
                    rprint(f"[red]Error loading {resource_type}:[/red] {e}")

        rprint(f"[green]Complete:[/green] {success} success, {errors} errors")


@app.command("stats")
def stats(
    url: str = typer.Option("http://localhost:8080", "--url", "-u", help="FHIR server base URL"),
) -> None:
    """Show statistics for a running FHIR server.

    Example:
        fhir server stats --url http://localhost:8080
    """
    import httpx

    resource_types = [
        "Patient",
        "Practitioner",
        "Organization",
        "Encounter",
        "Condition",
        "Observation",
        "MedicationRequest",
        "Procedure",
        "ValueSet",
        "CodeSystem",
        "Library",
    ]

    rprint("[bold]FHIR Server Statistics[/bold]")
    rprint(f"URL: {url}")
    rprint()

    table = Table(title="Resource Counts")
    table.add_column("Resource Type", style="cyan")
    table.add_column("Count", justify="right")

    total = 0
    try:
        with httpx.Client(timeout=10.0) as client:
            for rt in resource_types:
                try:
                    response = client.get(
                        f"{url}/{rt}",
                        params={"_count": 0, "_total": "accurate"},
                        headers={"Accept": "application/fhir+json"},
                    )
                    if response.status_code == 200:
                        data = response.json()
                        count = data.get("total", 0)
                        if count > 0:
                            table.add_row(rt, str(count))
                            total += count
                except Exception:
                    pass

        table.add_row("─" * 20, "─" * 8)
        table.add_row("[bold]Total[/bold]", f"[bold]{total}[/bold]")
        rprint(table)

    except httpx.RequestError as e:
        rprint(f"[red]Connection error:[/red] {e}")
        raise typer.Exit(1)


@app.command("info")
def info(
    url: str = typer.Option("http://localhost:8080", "--url", "-u", help="FHIR server base URL"),
) -> None:
    """Show server capability statement information.

    Example:
        fhir server info --url http://localhost:8080
    """
    import httpx

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                f"{url}/metadata",
                headers={"Accept": "application/fhir+json"},
            )

        if response.status_code != 200:
            rprint(f"[red]Error:[/red] Server returned {response.status_code}")
            raise typer.Exit(1)

        capability = response.json()

        rprint("[bold]FHIR Server Information[/bold]")
        rprint()
        rprint(f"  Name:         {capability.get('name', 'Unknown')}")
        rprint(f"  Publisher:    {capability.get('publisher', 'Unknown')}")
        rprint(f"  FHIR Version: {capability.get('fhirVersion', 'Unknown')}")
        rprint(f"  Status:       {capability.get('status', 'Unknown')}")
        rprint()

        # Show supported resources
        rest = capability.get("rest", [{}])[0]
        resources = rest.get("resource", [])

        if resources:
            table = Table(title="Supported Resources")
            table.add_column("Type", style="cyan")
            table.add_column("Interactions")
            table.add_column("Search Params")

            for r in resources:
                interactions = ", ".join(i.get("code", "") for i in r.get("interaction", []))
                search_params = len(r.get("searchParam", []))
                table.add_row(r.get("type", ""), interactions[:40], str(search_params))

            rprint(table)

    except httpx.RequestError as e:
        rprint(f"[red]Connection error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
