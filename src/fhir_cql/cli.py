"""Unified FHIR CLI - Command line interface for FHIRPath, CQL, ELM, and CDS Hooks."""

import typer

from fhir_cql.cds_cli import app as cds_app
from fhir_cql.cql_cli import app as cql_app
from fhir_cql.elm_cli import app as elm_app
from fhir_cql.fhirpath_cli import app as fhirpath_app

app = typer.Typer(
    name="fhir",
    help="FHIR tooling: FHIRPath expressions, CQL (Clinical Quality Language), ELM, and CDS Hooks",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(cql_app, name="cql", help="CQL parser, evaluator, and quality measures")
app.add_typer(elm_app, name="elm", help="ELM (Expression Logical Model) loader and evaluator")
app.add_typer(fhirpath_app, name="fhirpath", help="FHIRPath expression parser and evaluator")
app.add_typer(cds_app, name="cds", help="CDS Hooks server and configuration tools")


if __name__ == "__main__":
    app()
