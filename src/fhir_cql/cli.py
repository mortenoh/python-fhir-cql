"""Unified FHIR CLI - Command line interface for FHIRPath and CQL."""

import typer

from fhir_cql.cql_cli import app as cql_app
from fhir_cql.fhirpath_cli import app as fhirpath_app

app = typer.Typer(
    name="fhir",
    help="FHIR tooling: FHIRPath expressions and CQL (Clinical Quality Language)",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(cql_app, name="cql", help="CQL parser, evaluator, and quality measures")
app.add_typer(fhirpath_app, name="fhirpath", help="FHIRPath expression parser and evaluator")


if __name__ == "__main__":
    app()
