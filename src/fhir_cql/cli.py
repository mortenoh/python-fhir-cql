"""Unified FHIR CLI - Command line interface for FHIRPath, CQL, ELM, CDS Hooks, and Terminology."""

import typer

from fhir_cql.cds_cli import app as cds_app
from fhir_cql.cql_cli import app as cql_app
from fhir_cql.elm_cli import app as elm_app
from fhir_cql.fhirpath_cli import app as fhirpath_app
from fhir_cql.terminology_cli import app as terminology_app

app = typer.Typer(
    name="fhir",
    help="FHIR tooling: FHIRPath, CQL, ELM, CDS Hooks, and Terminology Service",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(cql_app, name="cql", help="CQL parser, evaluator, and quality measures")
app.add_typer(elm_app, name="elm", help="ELM (Expression Logical Model) loader and evaluator")
app.add_typer(fhirpath_app, name="fhirpath", help="FHIRPath expression parser and evaluator")
app.add_typer(cds_app, name="cds", help="CDS Hooks server and configuration tools")
app.add_typer(terminology_app, name="terminology", help="FHIR Terminology Service")


if __name__ == "__main__":
    app()
