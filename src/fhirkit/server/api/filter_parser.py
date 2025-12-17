"""FHIR _filter parameter parser and evaluator.

Implements the FHIR search filter syntax per:
https://hl7.org/fhir/search_filter.html

Supports:
- Comparison operators: eq, ne, gt, lt, ge, le, co, sw, ew, sa, eb, ap
- Logical operators: and, or, not
- Parentheses for grouping
- String values (quoted or unquoted)
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any


class FilterOp(Enum):
    """Filter comparison operators."""

    EQ = "eq"  # equals
    NE = "ne"  # not equals
    GT = "gt"  # greater than
    LT = "lt"  # less than
    GE = "ge"  # greater or equal
    LE = "le"  # less or equal
    CO = "co"  # contains
    SW = "sw"  # starts with
    EW = "ew"  # ends with
    SA = "sa"  # starts after
    EB = "eb"  # ends before
    AP = "ap"  # approximately


class LogicalOp(Enum):
    """Logical operators."""

    AND = "and"
    OR = "or"
    NOT = "not"


@dataclass
class FilterCondition:
    """A single filter condition."""

    path: str
    op: FilterOp
    value: str


@dataclass
class FilterExpression:
    """A filter expression (condition or logical combination)."""

    condition: FilterCondition | None = None
    logical_op: LogicalOp | None = None
    left: "FilterExpression | None" = None
    right: "FilterExpression | None" = None
    negated: bool = False


class FilterParser:
    """Parser for FHIR _filter expressions."""

    # Regex patterns
    TOKEN_PATTERN = re.compile(
        r"""
        (?P<lparen>\()|
        (?P<rparen>\))|
        (?P<string>"[^"]*")|
        (?P<word>[a-zA-Z_][a-zA-Z0-9_.-]*)|
        (?P<date>\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}(:\d{2})?)?)?)?)|
        (?P<number>-?\d+(\.\d+)?)|
        (?P<ws>\s+)
        """,
        re.VERBOSE,
    )

    COMPARISON_OPS = {"eq", "ne", "gt", "lt", "ge", "le", "co", "sw", "ew", "sa", "eb", "ap"}
    LOGICAL_OPS = {"and", "or", "not"}

    def __init__(self, expression: str):
        """Initialize parser with expression.

        Args:
            expression: The _filter expression string
        """
        self.expression = expression
        self.tokens: list[str] = []
        self.pos = 0
        self._tokenize()

    def _tokenize(self) -> None:
        """Tokenize the expression."""
        pos = 0
        while pos < len(self.expression):
            match = self.TOKEN_PATTERN.match(self.expression, pos)
            if not match:
                raise ValueError(f"Invalid token at position {pos}: {self.expression[pos:]}")

            if match.group("ws"):
                pos = match.end()
                continue

            if match.group("string"):
                # Remove quotes
                self.tokens.append(match.group("string")[1:-1])
            elif match.group("word"):
                self.tokens.append(match.group("word").lower())
            elif match.group("date"):
                self.tokens.append(match.group("date"))
            elif match.group("number"):
                self.tokens.append(match.group("number"))
            elif match.group("lparen"):
                self.tokens.append("(")
            elif match.group("rparen"):
                self.tokens.append(")")

            pos = match.end()

    def parse(self) -> FilterExpression:
        """Parse the expression.

        Returns:
            Parsed FilterExpression
        """
        if not self.tokens:
            raise ValueError("Empty filter expression")

        result = self._parse_or()

        if self.pos < len(self.tokens):
            raise ValueError(f"Unexpected token at position {self.pos}: {self.tokens[self.pos]}")

        return result

    def _current(self) -> str | None:
        """Get current token."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self) -> str | None:
        """Advance to next token and return previous."""
        token = self._current()
        self.pos += 1
        return token

    def _parse_or(self) -> FilterExpression:
        """Parse OR expressions (lowest precedence)."""
        left = self._parse_and()

        while self._current() == "or":
            self._advance()  # consume 'or'
            right = self._parse_and()
            left = FilterExpression(logical_op=LogicalOp.OR, left=left, right=right)

        return left

    def _parse_and(self) -> FilterExpression:
        """Parse AND expressions."""
        left = self._parse_not()

        while self._current() == "and":
            self._advance()  # consume 'and'
            right = self._parse_not()
            left = FilterExpression(logical_op=LogicalOp.AND, left=left, right=right)

        return left

    def _parse_not(self) -> FilterExpression:
        """Parse NOT expressions."""
        if self._current() == "not":
            self._advance()  # consume 'not'
            expr = self._parse_primary()
            return FilterExpression(logical_op=LogicalOp.NOT, left=expr, negated=True)

        return self._parse_primary()

    def _parse_primary(self) -> FilterExpression:
        """Parse primary expressions (conditions or parenthesized)."""
        if self._current() == "(":
            self._advance()  # consume '('
            expr = self._parse_or()
            if self._current() != ")":
                raise ValueError("Expected closing parenthesis")
            self._advance()  # consume ')'
            return expr

        return self._parse_condition()

    def _parse_condition(self) -> FilterExpression:
        """Parse a single condition: path op value."""
        path = self._advance()
        if not path or path in self.LOGICAL_OPS or path in ("(", ")"):
            raise ValueError(f"Expected path, got: {path}")

        op_str = self._advance()
        if not op_str or op_str not in self.COMPARISON_OPS:
            raise ValueError(f"Expected comparison operator, got: {op_str}")

        value = self._advance()
        if value is None:
            raise ValueError("Expected value after operator")

        try:
            op = FilterOp(op_str)
        except ValueError:
            raise ValueError(f"Unknown operator: {op_str}")

        condition = FilterCondition(path=path, op=op, value=value)
        return FilterExpression(condition=condition)


class FilterEvaluator:
    """Evaluates filter expressions against FHIR resources."""

    def __init__(self, search_params: dict[str, dict[str, Any]]):
        """Initialize evaluator.

        Args:
            search_params: Search parameter definitions for the resource type
        """
        self.search_params = search_params

    def evaluate(self, resource: dict[str, Any], expr: FilterExpression) -> bool:
        """Evaluate a filter expression against a resource.

        Args:
            resource: FHIR resource to evaluate
            expr: Filter expression

        Returns:
            True if resource matches the expression
        """
        if expr.condition:
            return self._evaluate_condition(resource, expr.condition)

        if expr.logical_op == LogicalOp.AND and expr.left and expr.right:
            return self.evaluate(resource, expr.left) and self.evaluate(resource, expr.right)

        if expr.logical_op == LogicalOp.OR and expr.left and expr.right:
            return self.evaluate(resource, expr.left) or self.evaluate(resource, expr.right)

        if (expr.logical_op == LogicalOp.NOT or expr.negated) and expr.left:
            return not self.evaluate(resource, expr.left)

        return False

    def _evaluate_condition(self, resource: dict[str, Any], cond: FilterCondition) -> bool:
        """Evaluate a single condition.

        Args:
            resource: FHIR resource
            cond: Condition to evaluate

        Returns:
            True if condition matches
        """
        # Get the value from the resource
        resource_value = self._get_value(resource, cond.path)

        if resource_value is None:
            return cond.op == FilterOp.NE  # ne matches if value is missing

        # Handle multiple values (e.g., from arrays)
        if isinstance(resource_value, list):
            return any(self._compare(v, cond.op, cond.value) for v in resource_value)

        return self._compare(resource_value, cond.op, cond.value)

    def _get_value(self, resource: dict[str, Any], path: str) -> Any:
        """Get value from resource using path.

        Args:
            resource: FHIR resource
            path: Search parameter name or path

        Returns:
            Value(s) at the path
        """
        # Check if it's a known search parameter
        param_def = self.search_params.get(path)
        if param_def:
            fhir_path = param_def.get("path", path)
        else:
            # Use path directly (simple element access)
            fhir_path = path

        return self._extract_path(resource, fhir_path)

    def _extract_path(self, obj: Any, path: str) -> Any:
        """Extract value from object using dot-notation path.

        Args:
            obj: Object to extract from
            path: Dot-notation path

        Returns:
            Value at path or None
        """
        if obj is None:
            return None

        parts = path.split(".")
        current = obj

        for part in parts:
            if current is None:
                return None

            if isinstance(current, list):
                # Extract from all items in list
                values = []
                for item in current:
                    val = self._extract_path(item, ".".join([part] + parts[parts.index(part) + 1 :]))
                    if val is not None:
                        if isinstance(val, list):
                            values.extend(val)
                        else:
                            values.append(val)
                return values if values else None

            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None

        return current

    def _compare(self, resource_val: Any, op: FilterOp, filter_val: str) -> bool:
        """Compare a resource value with a filter value.

        Args:
            resource_val: Value from resource
            op: Comparison operator
            filter_val: Value from filter

        Returns:
            True if comparison matches
        """
        # Convert resource value to string for comparison
        if isinstance(resource_val, bool):
            resource_str = str(resource_val).lower()
        elif isinstance(resource_val, dict):
            # Handle CodeableConcept, Coding, etc.
            resource_str = self._extract_code_value(resource_val)
        else:
            resource_str = str(resource_val).lower()

        filter_str = filter_val.lower()

        if op == FilterOp.EQ:
            return resource_str == filter_str

        if op == FilterOp.NE:
            return resource_str != filter_str

        if op == FilterOp.CO:
            return filter_str in resource_str

        if op == FilterOp.SW:
            return resource_str.startswith(filter_str)

        if op == FilterOp.EW:
            return resource_str.endswith(filter_str)

        # Numeric/date comparisons
        try:
            res_num = float(resource_str) if resource_str else 0
            flt_num = float(filter_str) if filter_str else 0

            if op == FilterOp.GT:
                return res_num > flt_num
            if op == FilterOp.LT:
                return res_num < flt_num
            if op == FilterOp.GE:
                return res_num >= flt_num
            if op == FilterOp.LE:
                return res_num <= flt_num
            if op == FilterOp.AP:
                # Approximately equal (within 10%)
                if flt_num == 0:
                    return res_num == 0
                return abs(res_num - flt_num) / abs(flt_num) <= 0.1

        except ValueError:
            # String comparison for dates, etc.
            if op == FilterOp.GT:
                return resource_str > filter_str
            if op == FilterOp.LT:
                return resource_str < filter_str
            if op == FilterOp.GE:
                return resource_str >= filter_str
            if op == FilterOp.LE:
                return resource_str <= filter_str
            if op in (FilterOp.SA, FilterOp.EB, FilterOp.AP):
                # Date period comparisons - simplified
                return resource_str >= filter_str if op == FilterOp.SA else resource_str <= filter_str

        return False

    def _extract_code_value(self, obj: dict[str, Any]) -> str:
        """Extract code value from CodeableConcept or Coding.

        Args:
            obj: CodeableConcept or Coding object

        Returns:
            Code value as string
        """
        # Try coding array first (CodeableConcept)
        if "coding" in obj:
            codings = obj["coding"]
            if codings and isinstance(codings, list):
                for coding in codings:
                    if "code" in coding:
                        return str(coding["code"]).lower()

        # Try direct code (Coding)
        if "code" in obj:
            return str(obj["code"]).lower()

        # Try value for simple types
        if "value" in obj:
            return str(obj["value"]).lower()

        return ""


def parse_filter(expression: str) -> FilterExpression:
    """Parse a _filter expression.

    Args:
        expression: Filter expression string

    Returns:
        Parsed FilterExpression

    Raises:
        ValueError: If expression is invalid
    """
    parser = FilterParser(expression)
    return parser.parse()


def apply_filter(
    resources: list[dict[str, Any]],
    expression: str,
    search_params: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Apply a _filter expression to filter resources.

    Args:
        resources: List of resources to filter
        expression: Filter expression string
        search_params: Search parameter definitions

    Returns:
        Filtered list of resources
    """
    if not expression:
        return resources

    parsed = parse_filter(expression)
    evaluator = FilterEvaluator(search_params)

    return [r for r in resources if evaluator.evaluate(r, parsed)]
