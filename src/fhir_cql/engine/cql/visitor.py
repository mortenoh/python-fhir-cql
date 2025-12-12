"""CQL Evaluator Visitor.

This module implements the ANTLR visitor pattern for CQL evaluation.
It walks the parse tree and evaluates expressions.
"""

import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

from antlr4 import ParseTreeVisitor

# Add generated directory to path
_gen_path = str(Path(__file__).parent.parent.parent.parent.parent / "generated" / "cql")
if _gen_path not in sys.path:
    sys.path.insert(0, _gen_path)

from cqlParser import cqlParser  # noqa: E402
from cqlVisitor import cqlVisitor  # noqa: E402

from ..exceptions import CQLError  # noqa: E402
from ..types import FHIRDate, FHIRDateTime, FHIRTime, Quantity  # noqa: E402
from .context import CQLContext  # noqa: E402
from .library import (  # noqa: E402
    CodeDefinition,
    CodeSystemDefinition,
    ConceptDefinition,
    CQLLibrary,
    ExpressionDefinition,
    FunctionDefinition,
    IncludeDefinition,
    ParameterDefinition,
    UsingDefinition,
    ValueSetDefinition,
)
from .types import CQLCode, CQLConcept, CQLInterval, CQLRatio, CQLTuple  # noqa: E402


class CQLEvaluatorVisitor(cqlVisitor):
    """Visitor that evaluates CQL expressions.

    This visitor implements the evaluation logic for CQL by walking
    the ANTLR parse tree and computing values.
    """

    def __init__(self, context: CQLContext | None = None):
        """Initialize the visitor.

        Args:
            context: CQL evaluation context
        """
        self.context = context or CQLContext()
        self._library: CQLLibrary | None = None

    @property
    def library(self) -> CQLLibrary | None:
        """Get the current library."""
        return self._library

    def evaluate(self, tree: Any) -> Any:
        """Evaluate a parse tree and return the result."""
        return self.visit(tree)

    # =========================================================================
    # Library Structure
    # =========================================================================

    def visitLibrary(self, ctx: cqlParser.LibraryContext) -> CQLLibrary:
        """Visit a library and build CQLLibrary structure."""
        # Get library definition
        lib_def = ctx.libraryDefinition()
        if lib_def:
            name, version = self.visit(lib_def)
        else:
            name, version = "Anonymous", None

        self._library = CQLLibrary(name=name, version=version)

        # Process all definitions in the library
        for child in ctx.children or []:
            if isinstance(child, cqlParser.LibraryDefinitionContext):
                continue  # Already processed
            result = self.visit(child)
            if result is not None:
                self._process_library_element(result)

        return self._library

    def _process_library_element(self, element: Any) -> None:
        """Process a library element and add it to the library."""
        if self._library is None:
            return

        if isinstance(element, UsingDefinition):
            self._library.using.append(element)
        elif isinstance(element, IncludeDefinition):
            self._library.includes.append(element)
        elif isinstance(element, CodeSystemDefinition):
            self._library.codesystems[element.name] = element
        elif isinstance(element, ValueSetDefinition):
            self._library.valuesets[element.name] = element
        elif isinstance(element, CodeDefinition):
            self._library.codes[element.name] = element
        elif isinstance(element, ConceptDefinition):
            self._library.concepts[element.name] = element
        elif isinstance(element, ParameterDefinition):
            self._library.parameters[element.name] = element
        elif isinstance(element, ExpressionDefinition):
            self._library.definitions[element.name] = element
        elif isinstance(element, FunctionDefinition):
            self._library.add_function(element)
        elif isinstance(element, str) and element.startswith("context:"):
            # Context definition
            ctx_name = element[8:]
            if ctx_name not in self._library.contexts:
                self._library.contexts.append(ctx_name)
            self._library.current_context = ctx_name

    def visitLibraryDefinition(self, ctx: cqlParser.LibraryDefinitionContext) -> tuple[str, str | None]:
        """Visit library definition and extract name and version."""
        name_ctx = ctx.qualifiedIdentifier()
        name = self._get_identifier_text(name_ctx)

        version = None
        version_ctx = ctx.versionSpecifier()
        if version_ctx:
            version = self._unquote_string(version_ctx.getText())

        return name, version

    def visitUsingDefinition(self, ctx: cqlParser.UsingDefinitionContext) -> UsingDefinition:
        """Visit using definition."""
        # UsingDefinition uses qualifiedIdentifier for the model name
        model_id = ctx.qualifiedIdentifier()
        model = self._get_identifier_text(model_id)

        version = None
        version_ctx = ctx.versionSpecifier()
        if version_ctx:
            version = self._unquote_string(version_ctx.getText())

        return UsingDefinition(model=model, version=version)

    def visitIncludeDefinition(self, ctx: cqlParser.IncludeDefinitionContext) -> IncludeDefinition:
        """Visit include definition."""
        lib_id = ctx.qualifiedIdentifier()
        library = self._get_identifier_text(lib_id)

        version = None
        version_ctx = ctx.versionSpecifier()
        if version_ctx:
            version = self._unquote_string(version_ctx.getText())

        alias = None
        local_id = ctx.localIdentifier()
        if local_id:
            alias = self._get_identifier_text(local_id)

        return IncludeDefinition(library=library, version=version, alias=alias)

    def visitParameterDefinition(self, ctx: cqlParser.ParameterDefinitionContext) -> ParameterDefinition:
        """Visit parameter definition."""
        name = self._get_identifier_text(ctx.identifier())

        type_spec = None
        type_ctx = ctx.typeSpecifier()
        if type_ctx:
            type_spec = type_ctx.getText()

        default_value = None
        expr = ctx.expression()
        if expr:
            default_value = self.visit(expr)

        return ParameterDefinition(name=name, type_specifier=type_spec, default_value=default_value)

    def visitCodesystemDefinition(self, ctx: cqlParser.CodesystemDefinitionContext) -> CodeSystemDefinition:
        """Visit codesystem definition."""
        name = self._get_identifier_text(ctx.identifier())
        cs_id = self._unquote_string(ctx.codesystemId().getText())

        version = None
        version_ctx = ctx.versionSpecifier()
        if version_ctx:
            version = self._unquote_string(version_ctx.getText())

        return CodeSystemDefinition(name=name, id=cs_id, version=version)

    def visitValuesetDefinition(self, ctx: cqlParser.ValuesetDefinitionContext) -> ValueSetDefinition:
        """Visit valueset definition."""
        name = self._get_identifier_text(ctx.identifier())
        vs_id = self._unquote_string(ctx.valuesetId().getText())

        version = None
        version_ctx = ctx.versionSpecifier()
        if version_ctx:
            version = self._unquote_string(version_ctx.getText())

        codesystems: list[str] = []
        cs_ctx = ctx.codesystems()
        if cs_ctx:
            for cs_id in cs_ctx.codesystemIdentifier():
                codesystems.append(self._get_identifier_text(cs_id))

        return ValueSetDefinition(name=name, id=vs_id, version=version, codesystems=codesystems)

    def visitCodeDefinition(self, ctx: cqlParser.CodeDefinitionContext) -> CodeDefinition:
        """Visit code definition."""
        name = self._get_identifier_text(ctx.identifier())
        code = self._unquote_string(ctx.codeId().getText())
        codesystem = self._get_identifier_text(ctx.codesystemIdentifier())

        display = None
        display_ctx = ctx.displayClause() if hasattr(ctx, "displayClause") else None
        if display_ctx:
            display = self._unquote_string(display_ctx.STRING().getText())

        return CodeDefinition(name=name, code=code, codesystem=codesystem, display=display)

    def visitConceptDefinition(self, ctx: cqlParser.ConceptDefinitionContext) -> ConceptDefinition:
        """Visit concept definition."""
        name = self._get_identifier_text(ctx.identifier())

        codes = []
        for code_id in ctx.codeIdentifier():
            codes.append(self._get_identifier_text(code_id))

        display = None
        display_ctx = ctx.displayClause() if hasattr(ctx, "displayClause") else None
        if display_ctx:
            display = self._unquote_string(display_ctx.STRING().getText())

        return ConceptDefinition(name=name, codes=codes, display=display)

    def visitContextDefinition(self, ctx: cqlParser.ContextDefinitionContext) -> str:
        """Visit context definition."""
        context_name = self._get_identifier_text(ctx.identifier())
        return f"context:{context_name}"

    def visitExpressionDefinition(self, ctx: cqlParser.ExpressionDefinitionContext) -> ExpressionDefinition:
        """Visit expression definition (define statement)."""
        name = self._get_identifier_text(ctx.identifier())

        access_modifier = None
        access_ctx = ctx.accessModifier()
        if access_ctx:
            access_modifier = access_ctx.getText()

        # Store the expression tree for later evaluation
        expr = ctx.expression()

        return ExpressionDefinition(
            name=name,
            access_modifier=access_modifier,
            expression_tree=expr,
            context=self._library.current_context if self._library else None,
        )

    def visitFunctionDefinition(self, ctx: cqlParser.FunctionDefinitionContext) -> FunctionDefinition:
        """Visit function definition."""
        name = self._get_identifier_text(ctx.identifierOrFunctionIdentifier())

        parameters = []
        for operand in ctx.operandDefinition():
            param_name = self._get_identifier_text(operand.referentialIdentifier())
            param_type = operand.typeSpecifier().getText() if operand.typeSpecifier() else "Any"
            parameters.append((param_name, param_type))

        return_type = None
        return_ctx = ctx.typeSpecifier()
        if return_ctx:
            return_type = return_ctx.getText()

        fluent = ctx.fluentModifier() is not None
        external = ctx.functionBody() is None or "external" in ctx.getText()

        body = ctx.functionBody()
        body_tree = body.expression() if body else None

        return FunctionDefinition(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body_tree=body_tree,
            fluent=fluent,
            external=external,
        )

    # =========================================================================
    # Literals
    # =========================================================================

    def visitLiteralTerm(self, ctx: cqlParser.LiteralTermContext) -> Any:
        """Visit a literal term."""
        return self.visit(ctx.literal())

    def visitBooleanLiteral(self, ctx: cqlParser.BooleanLiteralContext) -> bool:
        """Visit a boolean literal."""
        return ctx.getText().lower() == "true"

    def visitNullLiteral(self, ctx: cqlParser.NullLiteralContext) -> None:
        """Visit a null literal."""
        return None

    def visitStringLiteral(self, ctx: cqlParser.StringLiteralContext) -> str:
        """Visit a string literal."""
        return self._unquote_string(ctx.getText())

    def visitNumberLiteral(self, ctx: cqlParser.NumberLiteralContext) -> int | Decimal:
        """Visit a number literal."""
        text = ctx.getText()
        if "." in text:
            return Decimal(text)
        return int(text)

    def visitLongNumberLiteral(self, ctx: cqlParser.LongNumberLiteralContext) -> int:
        """Visit a long number literal."""
        text = ctx.getText()
        # Remove 'L' suffix if present
        if text.endswith("L"):
            text = text[:-1]
        return int(text)

    def visitDateTimeLiteral(self, ctx: cqlParser.DateTimeLiteralContext) -> FHIRDateTime | None:
        """Visit a datetime literal (@YYYY-MM-DDThh:mm:ss)."""
        text = ctx.getText()
        return FHIRDateTime.parse(text)

    def visitDateLiteral(self, ctx: cqlParser.DateLiteralContext) -> FHIRDate | None:
        """Visit a date literal (@YYYY-MM-DD)."""
        text = ctx.getText()
        # Remove @ prefix
        if text.startswith("@"):
            text = text[1:]
        return FHIRDate.parse(text)

    def visitTimeLiteral(self, ctx: cqlParser.TimeLiteralContext) -> FHIRTime | None:
        """Visit a time literal (@Thh:mm:ss)."""
        text = ctx.getText()
        # Remove @T prefix
        if text.startswith("@T"):
            text = text[2:]
        elif text.startswith("@"):
            text = text[1:]
        return FHIRTime.parse(text)

    def visitQuantityLiteral(self, ctx: cqlParser.QuantityLiteralContext) -> Quantity:
        """Visit a quantity literal (e.g., 10 'mg')."""
        quantity_ctx = ctx.quantity()
        return self.visitQuantity(quantity_ctx)

    def visitQuantity(self, ctx: cqlParser.QuantityContext) -> Quantity:
        """Visit a quantity value."""
        number_text = ctx.NUMBER().getText()
        value = Decimal(number_text) if "." in number_text else Decimal(int(number_text))

        unit = "1"  # Default unit
        unit_ctx = ctx.unit()
        if unit_ctx:
            unit = self._unquote_string(unit_ctx.getText())

        return Quantity(value=value, unit=unit)

    def visitRatioLiteral(self, ctx: cqlParser.RatioLiteralContext) -> CQLRatio:
        """Visit a ratio literal (e.g., 1:10)."""
        ratio_ctx = ctx.ratio()
        return self.visitRatio(ratio_ctx)

    def visitRatio(self, ctx: cqlParser.RatioContext) -> CQLRatio:
        """Visit a ratio value."""
        quantities = ctx.quantity()
        numerator = self.visitQuantity(quantities[0])
        denominator = self.visitQuantity(quantities[1])
        return CQLRatio(numerator=numerator, denominator=denominator)

    # =========================================================================
    # Selectors (Constructors)
    # =========================================================================

    def visitIntervalSelectorTerm(self, ctx: cqlParser.IntervalSelectorTermContext) -> CQLInterval[Any]:
        """Visit interval selector term."""
        return self.visit(ctx.intervalSelector())

    def visitIntervalSelector(self, ctx: cqlParser.IntervalSelectorContext) -> CQLInterval[Any]:
        """Visit interval selector (Interval[low, high])."""
        # Determine if bounds are open or closed
        text = ctx.getText()
        low_closed = text.startswith("Interval[")
        high_closed = text.endswith("]")

        # Get the expressions
        expressions = ctx.expression()
        low = self.visit(expressions[0]) if len(expressions) > 0 else None
        high = self.visit(expressions[1]) if len(expressions) > 1 else None

        return CQLInterval(low=low, high=high, low_closed=low_closed, high_closed=high_closed)

    def visitListSelectorTerm(self, ctx: cqlParser.ListSelectorTermContext) -> list[Any]:
        """Visit list selector term."""
        return self.visit(ctx.listSelector())

    def visitListSelector(self, ctx: cqlParser.ListSelectorContext) -> list[Any]:
        """Visit list selector ({ item1, item2, ... })."""
        result = []
        for expr in ctx.expression():
            result.append(self.visit(expr))
        return result

    def visitTupleSelectorTerm(self, ctx: cqlParser.TupleSelectorTermContext) -> CQLTuple:
        """Visit tuple selector term."""
        return self.visit(ctx.tupleSelector())

    def visitTupleSelector(self, ctx: cqlParser.TupleSelectorContext) -> CQLTuple:
        """Visit tuple selector (Tuple { element1: value1, ... })."""
        elements: dict[str, Any] = {}
        for element in ctx.tupleElementSelector():
            name = self._get_identifier_text(element.referentialIdentifier())
            value = self.visit(element.expression())
            elements[name] = value
        return CQLTuple(elements=elements)

    def visitCodeSelectorTerm(self, ctx: cqlParser.CodeSelectorTermContext) -> CQLCode:
        """Visit code selector term."""
        return self.visit(ctx.codeSelector())

    def visitCodeSelector(self, ctx: cqlParser.CodeSelectorContext) -> CQLCode:
        """Visit code selector (Code 'code' from "system")."""
        code = self._unquote_string(ctx.STRING().getText())
        system_ctx = ctx.codesystemIdentifier()

        # Resolve codesystem
        if self._library and system_ctx:
            cs_name = self._get_identifier_text(system_ctx)
            cs_def = self._library.codesystems.get(cs_name)
            if cs_def:
                system = cs_def.id
            else:
                system = cs_name
        else:
            system = ""

        display = None
        display_ctx = ctx.displayClause() if hasattr(ctx, "displayClause") else None
        if display_ctx:
            display = self._unquote_string(display_ctx.STRING().getText())

        return CQLCode(code=code, system=system, display=display)

    def visitConceptSelectorTerm(self, ctx: cqlParser.ConceptSelectorTermContext) -> CQLConcept:
        """Visit concept selector term."""
        return self.visit(ctx.conceptSelector())

    def visitConceptSelector(self, ctx: cqlParser.ConceptSelectorContext) -> CQLConcept:
        """Visit concept selector (Concept { code1, code2 })."""
        codes = []
        for code_selector in ctx.codeSelector():
            codes.append(self.visit(code_selector))

        display = None
        display_ctx = ctx.displayClause() if hasattr(ctx, "displayClause") else None
        if display_ctx:
            display = self._unquote_string(display_ctx.STRING().getText())

        return CQLConcept(codes=tuple(codes), display=display)

    # =========================================================================
    # Expression Terms
    # =========================================================================

    def visitTermExpression(self, ctx: cqlParser.TermExpressionContext) -> Any:
        """Visit a term expression."""
        return self.visit(ctx.expressionTerm())

    def visitTermExpressionTerm(self, ctx: cqlParser.TermExpressionTermContext) -> Any:
        """Visit a term expression term."""
        return self.visit(ctx.term())

    def visitParenthesizedTerm(self, ctx: cqlParser.ParenthesizedTermContext) -> Any:
        """Visit a parenthesized term."""
        return self.visit(ctx.expression())

    def visitExternalConstantTerm(self, ctx: cqlParser.ExternalConstantTermContext) -> Any:
        """Visit external constant (%name)."""
        return self.visit(ctx.externalConstant())

    def visitExternalConstant(self, ctx: cqlParser.ExternalConstantContext) -> Any:
        """Visit external constant."""
        name = ctx.getText()[1:]  # Remove % prefix
        return self.context.get_constant(name)

    # =========================================================================
    # Arithmetic Operations
    # =========================================================================

    def visitAdditionExpressionTerm(self, ctx: cqlParser.AdditionExpressionTermContext) -> Any:
        """Visit addition/subtraction expression."""
        left = self.visit(ctx.expressionTerm(0))
        right = self.visit(ctx.expressionTerm(1))
        op = ctx.getChild(1).getText()

        # String concatenation handles null specially
        if op == "&":
            # In CQL, null is treated as empty string in string concatenation
            left_str = str(left) if left is not None else ""
            right_str = str(right) if right is not None else ""
            return left_str + right_str

        if left is None or right is None:
            return None

        if op == "+":
            return self._add(left, right)
        elif op == "-":
            return self._subtract(left, right)

        return None

    def visitMultiplicationExpressionTerm(self, ctx: cqlParser.MultiplicationExpressionTermContext) -> Any:
        """Visit multiplication/division expression."""
        left = self.visit(ctx.expressionTerm(0))
        right = self.visit(ctx.expressionTerm(1))
        op = ctx.getChild(1).getText()

        if left is None or right is None:
            return None

        if op == "*":
            return self._multiply(left, right)
        elif op == "/":
            return self._divide(left, right)
        elif op == "div":
            return self._truncated_divide(left, right)
        elif op == "mod":
            return self._modulo(left, right)

        return None

    def visitPowerExpressionTerm(self, ctx: cqlParser.PowerExpressionTermContext) -> Any:
        """Visit power expression (x ^ y)."""
        base = self.visit(ctx.expressionTerm(0))
        exponent = self.visit(ctx.expressionTerm(1))

        if base is None or exponent is None:
            return None

        return Decimal(base) ** Decimal(exponent)

    def visitPolarityExpressionTerm(self, ctx: cqlParser.PolarityExpressionTermContext) -> Any:
        """Visit polarity expression (+x or -x)."""
        value = self.visit(ctx.expressionTerm())
        op = ctx.getChild(0).getText()

        if value is None:
            return None

        if op == "-":
            if isinstance(value, Quantity):
                return Quantity(value=-value.value, unit=value.unit)
            return -value
        return value

    # =========================================================================
    # Boolean Operations
    # =========================================================================

    def visitAndExpression(self, ctx: cqlParser.AndExpressionContext) -> bool | None:
        """Visit AND expression with three-valued logic."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        return self._three_valued_and(left, right)

    def visitOrExpression(self, ctx: cqlParser.OrExpressionContext) -> bool | None:
        """Visit OR/XOR expression with three-valued logic."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText().lower()

        if op == "or":
            return self._three_valued_or(left, right)
        elif op == "xor":
            return self._three_valued_xor(left, right)

        return None

    def visitNotExpression(self, ctx: cqlParser.NotExpressionContext) -> bool | None:
        """Visit NOT expression."""
        value = self.visit(ctx.expression())
        if value is None:
            return None
        return not value

    def visitImpliesExpression(self, ctx: cqlParser.ImpliesExpressionContext) -> bool | None:
        """Visit IMPLIES expression."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        return self._three_valued_implies(left, right)

    def visitBooleanExpression(self, ctx: cqlParser.BooleanExpressionContext) -> bool | None:
        """Visit boolean IS/IS NOT expression."""
        value = self.visit(ctx.expression())
        text = ctx.getText().lower()

        # Check IS NOT patterns first (longer match)
        if "isnotnull" in text:
            return value is not None
        elif "isnull" in text:
            return value is None
        elif "isnottrue" in text:
            return value is not True
        elif "istrue" in text:
            return value is True
        elif "isnotfalse" in text:
            return value is not False
        elif "isfalse" in text:
            return value is False

        return None

    # =========================================================================
    # Comparison Operations
    # =========================================================================

    def visitEqualityExpression(self, ctx: cqlParser.EqualityExpressionContext) -> bool | None:
        """Visit equality expression (= or !=)."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()

        if left is None or right is None:
            return None

        if op == "=" or op == "~":
            return self._equals(left, right)
        elif op == "!=" or op == "!~":
            result = self._equals(left, right)
            return not result if result is not None else None

        return None

    def visitInequalityExpression(self, ctx: cqlParser.InequalityExpressionContext) -> bool | None:
        """Visit inequality expression (<, <=, >, >=)."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()

        if left is None or right is None:
            return None

        if op == "<":
            return left < right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == ">=":
            return left >= right

        return None

    # =========================================================================
    # Conditional Expressions
    # =========================================================================

    def visitIfThenElseExpressionTerm(self, ctx: cqlParser.IfThenElseExpressionTermContext) -> Any:
        """Visit if-then-else expression."""
        condition = self.visit(ctx.expression(0))

        if condition is True:
            return self.visit(ctx.expression(1))
        else:
            return self.visit(ctx.expression(2))

    def visitCaseExpressionTerm(self, ctx: cqlParser.CaseExpressionTermContext) -> Any:
        """Visit case expression."""
        # Check if this is a simple case (with comparand) or searched case
        comparand = None
        if ctx.expression():
            comparand = self.visit(ctx.expression())

        for item in ctx.caseExpressionItem():
            when_expr = item.expression(0)
            then_expr = item.expression(1)

            when_value = self.visit(when_expr)

            if comparand is not None:
                # Simple case: compare with comparand
                if self._equals(comparand, when_value):
                    return self.visit(then_expr)
            else:
                # Searched case: when_value should be boolean
                if when_value is True:
                    return self.visit(then_expr)

        # Return else clause if present
        else_expr = ctx.expression()
        if else_expr and ctx.getChildCount() > 0:
            # Find the else expression (last expression in context)
            expressions = [child for child in ctx.children if hasattr(child, "expression")]
            if expressions:
                return self.visit(expressions[-1])

        return None

    # =========================================================================
    # Invocations
    # =========================================================================

    def visitInvocationTerm(self, ctx: cqlParser.InvocationTermContext) -> Any:
        """Visit an invocation term."""
        return self.visit(ctx.invocation())

    def visitMemberInvocation(self, ctx: cqlParser.MemberInvocationContext) -> Any:
        """Visit member invocation (identifier access)."""
        name = self._get_identifier_text(ctx.referentialIdentifier())

        # Check if it's a query alias
        if self.context.has_alias(name):
            return self.context.get_alias(name)

        # Check if it's a parameter
        if self.context.has_parameter(name):
            return self.context.get_parameter(name)

        # Check if it's a definition
        if self._library and name in self._library.definitions:
            return self._evaluate_definition(name)

        # Check if it's a code reference
        if self._library and name in self._library.codes:
            return self._library.resolve_code(name)

        # Check if it's a concept reference
        if self._library and name in self._library.concepts:
            return self._library.resolve_concept(name)

        return None

    def visitFunctionInvocation(self, ctx: cqlParser.FunctionInvocationContext) -> Any:
        """Visit function invocation."""
        func_ctx = ctx.function()
        name = self._get_identifier_text(func_ctx.referentialIdentifier())

        # Evaluate arguments
        args = []
        param_list = func_ctx.paramList()
        if param_list:
            for expr in param_list.expression():
                args.append(self.visit(expr))

        return self._call_function(name, args)

    def visitInvocationExpressionTerm(self, ctx: cqlParser.InvocationExpressionTermContext) -> Any:
        """Visit invocation expression (method chaining)."""
        target = self.visit(ctx.expressionTerm())
        invocation = ctx.qualifiedInvocation()

        if isinstance(invocation, cqlParser.QualifiedMemberInvocationContext):
            # Property access on target
            name = self._get_identifier_text(invocation.referentialIdentifier())
            if isinstance(target, dict):
                return target.get(name)
            elif isinstance(target, CQLTuple):
                return target.elements.get(name)
            elif isinstance(target, list):
                # Flatten property access on list
                return [item.get(name) if isinstance(item, dict) else getattr(item, name, None) for item in target]
        elif isinstance(invocation, cqlParser.QualifiedFunctionInvocationContext):
            # Method call on target
            func_ctx = invocation.qualifiedFunction()
            name = self._get_identifier_text(func_ctx.identifierOrFunctionIdentifier())

            args = [target]
            param_list = func_ctx.paramList()
            if param_list:
                for expr in param_list.expression():
                    args.append(self.visit(expr))

            return self._call_function(name, args)

        return target

    def visitThisInvocation(self, ctx: cqlParser.ThisInvocationContext) -> Any:
        """Visit $this invocation."""
        return self.context.this

    def visitIndexInvocation(self, ctx: cqlParser.IndexInvocationContext) -> int | None:
        """Visit $index invocation."""
        return self.context.index

    def visitTotalInvocation(self, ctx: cqlParser.TotalInvocationContext) -> Any:
        """Visit $total invocation."""
        return self.context.total

    # =========================================================================
    # Existence/Membership
    # =========================================================================

    def visitExistenceExpression(self, ctx: cqlParser.ExistenceExpressionContext) -> bool:
        """Visit exists expression."""
        value = self.visit(ctx.expression())
        if isinstance(value, list):
            return len(value) > 0
        return value is not None

    def visitMembershipExpression(self, ctx: cqlParser.MembershipExpressionContext) -> bool | None:
        """Visit membership expression (in, contains)."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText().lower()

        if op == "in":
            if isinstance(right, list):
                return left in right
            elif isinstance(right, CQLInterval):
                return right.contains(left)
        elif op == "contains":
            if isinstance(left, list):
                return right in left
            elif isinstance(left, CQLInterval):
                return left.contains(right)

        return None

    def visitBetweenExpression(self, ctx: cqlParser.BetweenExpressionContext) -> bool | None:
        """Visit between expression (x between y and z)."""
        value = self.visit(ctx.expression())
        expressions = ctx.expressionTerm()
        low = self.visit(expressions[0])
        high = self.visit(expressions[1])

        if value is None or low is None or high is None:
            return None

        return low <= value <= high

    # =========================================================================
    # Type Operations
    # =========================================================================

    def visitTypeExpression(self, ctx: cqlParser.TypeExpressionContext) -> Any:
        """Visit type expression (is, as)."""
        value = self.visit(ctx.expression())
        type_name = ctx.typeSpecifier().getText()
        op = ctx.getChild(1).getText().lower()

        if op == "is":
            return self._check_type(value, type_name)
        elif op == "as":
            return self._cast_type(value, type_name)

        return value

    def visitCastExpression(self, ctx: cqlParser.CastExpressionContext) -> Any:
        """Visit cast expression."""
        value = self.visit(ctx.expression())
        type_name = ctx.typeSpecifier().getText()
        return self._cast_type(value, type_name)

    # =========================================================================
    # Query Expressions
    # =========================================================================

    def visitQueryExpression(self, ctx: cqlParser.QueryExpressionContext) -> list[Any]:
        """Visit query expression."""
        return self.visit(ctx.query())

    def visitQuery(self, ctx: cqlParser.QueryContext) -> list[Any]:
        """Visit a query and execute it."""
        # Get source clause
        source_clause = ctx.sourceClause()
        results = self._process_query_sources(source_clause)

        # Apply let clauses
        let_clause = ctx.letClause()
        if let_clause:
            results = self._apply_let_clause(results, let_clause)

        # Apply where clause
        where_clause = ctx.whereClause()
        if where_clause:
            results = self._apply_where_clause(results, where_clause)

        # Apply return clause
        return_clause = ctx.returnClause()
        if return_clause:
            results = self._apply_return_clause(results, return_clause)

        # Apply sort clause
        sort_clause = ctx.sortClause()
        if sort_clause:
            results = self._apply_sort_clause(results, sort_clause)

        return results

    def _process_query_sources(self, ctx: cqlParser.SourceClauseContext) -> list[Any]:
        """Process query source clause and return initial result set."""
        results: list[dict[str, Any]] = []

        for alias_def in ctx.aliasedQuerySource():
            source = alias_def.querySource()
            alias = self._get_identifier_text(alias_def.alias().identifier())

            # Evaluate the source expression
            source_value = self._evaluate_query_source(source)

            # Convert to list if necessary
            if not isinstance(source_value, list):
                source_value = [source_value] if source_value is not None else []

            # Initialize result set with source
            if not results:
                results = [{alias: item} for item in source_value]
            else:
                # Cross join with additional source
                new_results = []
                for existing in results:
                    for item in source_value:
                        combined = dict(existing)
                        combined[alias] = item
                        new_results.append(combined)
                results = new_results

        return results

    def _evaluate_query_source(self, ctx: cqlParser.QuerySourceContext) -> Any:
        """Evaluate a query source."""
        # Check if it's a retrieve
        retrieve = ctx.retrieve()
        if retrieve:
            return self.visit(retrieve)

        # Check if it's an expression
        expr = ctx.expression()
        if expr:
            return self.visit(expr)

        # Check if it's a qualified identifier expression (reference to definition)
        qual_id = ctx.qualifiedIdentifierExpression()
        if qual_id:
            name = self._get_identifier_text(qual_id)
            if self._library and name in self._library.definitions:
                return self._evaluate_definition(name)
            return self.context.get_alias(name)

        return None

    def _apply_let_clause(
        self, results: list[dict[str, Any]], ctx: cqlParser.LetClauseContext
    ) -> list[dict[str, Any]]:
        """Apply let clause to bind additional variables."""
        for let_item in ctx.letClauseItem():
            identifier = self._get_identifier_text(let_item.identifier())
            expr = let_item.expression()

            new_results = []
            for row in results:
                # Create context with current row aliases
                self.context.push_scope()
                for alias, value in row.items():
                    self.context.set_alias(alias, value)

                try:
                    let_value = self.visit(expr)
                    new_row = dict(row)
                    new_row[identifier] = let_value
                    new_results.append(new_row)
                finally:
                    self.context.pop_scope()

            results = new_results

        return results

    def _apply_where_clause(
        self, results: list[dict[str, Any]], ctx: cqlParser.WhereClauseContext
    ) -> list[dict[str, Any]]:
        """Apply where clause filter."""
        expr = ctx.expression()
        filtered = []

        for row in results:
            # Create context with current row aliases
            self.context.push_scope()
            for alias, value in row.items():
                self.context.set_alias(alias, value)

            try:
                condition = self.visit(expr)
                if condition is True:
                    filtered.append(row)
            finally:
                self.context.pop_scope()

        return filtered

    def _apply_return_clause(
        self, results: list[dict[str, Any]], ctx: cqlParser.ReturnClauseContext
    ) -> list[Any]:
        """Apply return clause to shape output."""
        expr = ctx.expression()
        distinct = ctx.getText().lower().startswith("return distinct") or ctx.getText().lower().startswith(
            "return all"
        )
        is_all = "all" in ctx.getText().lower()

        returned = []
        for row in results:
            # Create context with current row aliases
            self.context.push_scope()
            for alias, value in row.items():
                self.context.set_alias(alias, value)

            try:
                value = self.visit(expr)
                returned.append(value)
            finally:
                self.context.pop_scope()

        # Apply distinct if specified
        if distinct and not is_all:
            seen: list[Any] = []
            for item in returned:
                if item not in seen:
                    seen.append(item)
            return seen

        return returned

    def _apply_sort_clause(
        self, results: list[Any], ctx: cqlParser.SortClauseContext
    ) -> list[Any]:
        """Apply sort clause to order results."""
        sort_items = ctx.sortByItem()

        # Check for simple sort direction (sort asc / sort desc)
        if not sort_items:
            direction = ctx.sortDirection()
            if direction:
                dir_text = direction.getText().lower()
                reverse = dir_text in ("desc", "descending")
                try:
                    # Filter out None values for sorting, then sort
                    non_none = [r for r in results if r is not None]
                    none_count = len(results) - len(non_none)
                    sorted_results = sorted(non_none, reverse=reverse)
                    # Add None values at the end
                    return sorted_results + [None] * none_count
                except TypeError:
                    pass  # Keep original order if not sortable
            return results

        # Complex sort with sortByItem
        for sort_item in reversed(sort_items):  # Apply in reverse order
            direction = sort_item.sortDirection()
            dir_text = direction.getText().lower() if direction else "asc"
            reverse = dir_text in ("desc", "descending")

            expr = sort_item.expressionTerm()
            if expr:
                # Sort by expression
                def sort_key(item: Any) -> Any:
                    self.context.push_scope()
                    self.context.set_alias("$this", item)
                    try:
                        key = self.visit(expr)
                        return (key is None, key)  # None values sort last
                    finally:
                        self.context.pop_scope()

                try:
                    results = sorted(results, key=sort_key, reverse=reverse)
                except TypeError:
                    pass  # Keep original order if not sortable
            else:
                # Sort by natural order
                try:
                    results = sorted(results, reverse=reverse)
                except TypeError:
                    pass

        return results

    def visitRetrieve(self, ctx: cqlParser.RetrieveContext) -> list[Any]:
        """Visit retrieve expression [ResourceType: property in ValueSet]."""
        # Get resource type
        named_type = ctx.namedTypeSpecifier()
        if named_type:
            resource_type = self._get_identifier_text(named_type)
        else:
            resource_type = ctx.getText().split(":")[0].strip("[")

        # Get code filter if present
        context_expr = ctx.contextIdentifier() if hasattr(ctx, "contextIdentifier") else None
        terminology = ctx.terminology() if hasattr(ctx, "terminology") else None
        code_path = ctx.codePath() if hasattr(ctx, "codePath") else None

        # Build filter parameters
        filters: dict[str, Any] = {"resourceType": resource_type}

        if terminology:
            # Parse terminology reference (valueset or code)
            term_expr = terminology.qualifiedIdentifierExpression()
            if term_expr:
                term_name = self._get_identifier_text(term_expr)
                if self._library:
                    if term_name in self._library.valuesets:
                        filters["valueset"] = self._library.valuesets[term_name].id
                    elif term_name in self._library.codes:
                        code = self._library.resolve_code(term_name)
                        if code:
                            filters["code"] = code

        if code_path:
            filters["codePath"] = self._get_identifier_text(code_path)

        # Use data source if available
        if self.context.data_source:
            return self.context.data_source.retrieve(**filters)

        return []

    # =========================================================================
    # Set Operations
    # =========================================================================

    def visitInFixSetExpression(self, ctx: cqlParser.InFixSetExpressionContext) -> list[Any]:
        """Visit infix set expression (union, intersect, except)."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText().lower()

        if not isinstance(left, list):
            left = [left] if left is not None else []
        if not isinstance(right, list):
            right = [right] if right is not None else []

        if op == "union":
            # Union removes duplicates
            result = list(left)
            for item in right:
                if item not in result:
                    result.append(item)
            return result
        elif op == "intersect":
            return [item for item in left if item in right]
        elif op == "except":
            return [item for item in left if item not in right]

        return left

    # =========================================================================
    # Interval Operations
    # =========================================================================

    def visitTimingExpression(self, ctx: cqlParser.TimingExpressionContext) -> bool | None:
        """Visit timing expression (before, after, during, etc.)."""
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        # Get the operator
        op_text = ""
        for i in range(1, ctx.getChildCount() - 1):
            child = ctx.getChild(i)
            if hasattr(child, "getText"):
                op_text += child.getText().lower() + " "
        op_text = op_text.strip()

        if left is None or right is None:
            return None

        # Handle interval timing
        if isinstance(left, CQLInterval) and isinstance(right, CQLInterval):
            return self._interval_timing(left, right, op_text)
        elif isinstance(left, CQLInterval):
            return self._interval_point_timing(left, right, op_text)
        elif isinstance(right, CQLInterval):
            return self._point_interval_timing(left, right, op_text)

        # Handle point comparisons
        if "before" in op_text:
            return left < right
        elif "after" in op_text:
            return left > right

        return None

    def _interval_timing(self, left: CQLInterval[Any], right: CQLInterval[Any], op: str) -> bool | None:
        """Handle interval-to-interval timing comparisons."""
        if "before" in op:
            if left.high is None or right.low is None:
                return None
            return left.high < right.low
        elif "after" in op:
            if left.low is None or right.high is None:
                return None
            return left.low > right.high
        elif "meets" in op:
            if "before" in op:
                return left.high == right.low
            elif "after" in op:
                return left.low == right.high
            else:
                return left.high == right.low or left.low == right.high
        elif "overlaps" in op:
            return left.overlaps(right)
        elif "starts" in op:
            return left.low == right.low
        elif "ends" in op:
            return left.high == right.high
        elif "during" in op or "included in" in op:
            return right.includes(left)
        elif "includes" in op:
            return left.includes(right)
        elif "same" in op:
            return left == right
        return None

    def _interval_point_timing(self, interval: CQLInterval[Any], point: Any, op: str) -> bool | None:
        """Handle interval-to-point timing comparisons."""
        if "before" in op:
            return interval.high is not None and interval.high < point
        elif "after" in op:
            return interval.low is not None and interval.low > point
        elif "contains" in op or "includes" in op:
            return interval.contains(point)
        return None

    def _point_interval_timing(self, point: Any, interval: CQLInterval[Any], op: str) -> bool | None:
        """Handle point-to-interval timing comparisons."""
        if "before" in op:
            return interval.low is not None and point < interval.low
        elif "after" in op:
            return interval.high is not None and point > interval.high
        elif "during" in op or "in" in op or "included in" in op:
            return interval.contains(point)
        return None

    # =========================================================================
    # Indexing
    # =========================================================================

    def visitIndexedExpressionTerm(self, ctx: cqlParser.IndexedExpressionTermContext) -> Any:
        """Visit indexed expression (list[index])."""
        collection = self.visit(ctx.expressionTerm())
        index = self.visit(ctx.expression())

        if collection is None or index is None:
            return None

        if isinstance(collection, list):
            if isinstance(index, int) and 0 <= index < len(collection):
                return collection[index]
        elif isinstance(collection, str):
            if isinstance(index, int) and 0 <= index < len(collection):
                return collection[index]

        return None

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _get_identifier_text(self, ctx: Any) -> str:
        """Extract identifier text from various context types."""
        if ctx is None:
            return ""

        text = ctx.getText()

        # Handle quoted identifiers
        if text.startswith('"') and text.endswith('"'):
            return text[1:-1]
        if text.startswith("`") and text.endswith("`"):
            return text[1:-1]

        return text

    def _unquote_string(self, text: str) -> str:
        """Remove quotes from a string literal."""
        if len(text) >= 2:
            if (text.startswith("'") and text.endswith("'")) or (text.startswith('"') and text.endswith('"')):
                text = text[1:-1]
                # Handle escape sequences
                text = text.replace("\\'", "'")
                text = text.replace('\\"', '"')
                text = text.replace("\\\\", "\\")
                text = text.replace("\\n", "\n")
                text = text.replace("\\r", "\r")
                text = text.replace("\\t", "\t")
        return text

    def _evaluate_definition(self, name: str) -> Any:
        """Evaluate a named definition."""
        if not self._library:
            return None

        # Check cache
        found, cached = self.context.get_cached_definition(name)
        if found:
            return cached

        # Check for recursion
        if not self.context.start_evaluation(name):
            raise CQLError(f"Recursive definition detected: {name}")

        try:
            definition = self._library.definitions.get(name)
            if not definition or not definition.expression_tree:
                return None

            result = self.visit(definition.expression_tree)
            self.context.cache_definition(name, result)
            return result
        finally:
            self.context.end_evaluation(name)

    def _call_function(self, name: str, args: list[Any]) -> Any:
        """Call a function by name with arguments."""
        # Check for user-defined functions
        if self._library:
            func = self._library.get_function(name, len(args))
            if func and func.body_tree:
                return self._call_user_function(func, args)

        # Built-in functions - delegate to function registry
        # This will be implemented later with the function modules
        return self._call_builtin_function(name, args)

    def _call_user_function(self, func: FunctionDefinition, args: list[Any]) -> Any:
        """Call a user-defined function."""
        # Create new context with parameters bound
        child_ctx = self.context.child()
        for (param_name, _), arg_value in zip(func.parameters, args):
            child_ctx.set_alias(param_name, arg_value)

        # Save current context and switch
        old_ctx = self.context
        self.context = child_ctx

        try:
            result = self.visit(func.body_tree)
            return result
        finally:
            self.context = old_ctx

    def _call_builtin_function(self, name: str, args: list[Any]) -> Any:
        """Call a built-in function."""
        # Basic built-in functions for Phase 1
        name_lower = name.lower()

        if name_lower == "count":
            if args and isinstance(args[0], list):
                return len(args[0])
            return 0

        if name_lower == "exists":
            if args:
                val = args[0]
                if isinstance(val, list):
                    return len(val) > 0
                return val is not None
            return False

        if name_lower == "first":
            if args and isinstance(args[0], list) and len(args[0]) > 0:
                return args[0][0]
            return None

        if name_lower == "last":
            if args and isinstance(args[0], list) and len(args[0]) > 0:
                return args[0][-1]
            return None

        if name_lower == "length":
            if args:
                val = args[0]
                if isinstance(val, str):
                    return len(val)
                if isinstance(val, list):
                    return len(val)
            return None

        if name_lower == "tostring":
            if args and args[0] is not None:
                return str(args[0])
            return None

        if name_lower == "tointeger":
            if args and args[0] is not None:
                try:
                    return int(args[0])
                except (ValueError, TypeError):
                    return None
            return None

        if name_lower == "todecimal":
            if args and args[0] is not None:
                try:
                    return Decimal(str(args[0]))
                except (ValueError, TypeError):
                    return None
            return None

        if name_lower == "toboolean":
            if args and args[0] is not None:
                val = args[0]
                if isinstance(val, bool):
                    return val
                if isinstance(val, str):
                    return val.lower() in ("true", "t", "yes", "y", "1")
            return None

        if name_lower == "coalesce":
            for arg in args:
                if arg is not None:
                    if isinstance(arg, list):
                        if len(arg) > 0:
                            return arg
                    else:
                        return arg
            return None

        if name_lower == "isnull":
            return args[0] is None if args else True

        if name_lower in ("sum", "avg", "min", "max"):
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal))]
                if not values:
                    return None
                if name_lower == "sum":
                    return sum(values)
                if name_lower == "avg":
                    return sum(values) / len(values)
                if name_lower == "min":
                    return min(values)
                if name_lower == "max":
                    return max(values)
            return None

        # Phase 2: List functions
        if name_lower == "tail":
            if args and isinstance(args[0], list) and len(args[0]) > 0:
                return args[0][1:]
            return []

        if name_lower == "take":
            if len(args) >= 2 and isinstance(args[0], list):
                n = args[1]
                if n is None or n < 0:
                    return []
                return args[0][:n]
            return []

        if name_lower == "skip":
            if len(args) >= 2 and isinstance(args[0], list):
                n = args[1]
                if n is None or n < 0:
                    return args[0]
                return args[0][n:]
            return []

        if name_lower == "flatten":
            if args and isinstance(args[0], list):
                result = []
                for item in args[0]:
                    if isinstance(item, list):
                        result.extend(item)
                    else:
                        result.append(item)
                return result
            return []

        if name_lower == "distinct":
            if args and isinstance(args[0], list):
                seen: list[Any] = []
                for item in args[0]:
                    if item not in seen:
                        seen.append(item)
                return seen
            return []

        if name_lower == "sort":
            if args and isinstance(args[0], list):
                items = [i for i in args[0] if i is not None]
                try:
                    return sorted(items)
                except TypeError:
                    return items
            return []

        if name_lower == "indexof":
            if len(args) >= 2 and isinstance(args[0], list):
                try:
                    return args[0].index(args[1])
                except ValueError:
                    return -1
            return -1

        if name_lower == "singleton":
            if args and isinstance(args[0], list):
                if len(args[0]) == 1:
                    return args[0][0]
                elif len(args[0]) == 0:
                    return None
                else:
                    raise CQLError("Expected single element but found multiple")
            return args[0] if args else None

        if name_lower == "alltrue":
            if args and isinstance(args[0], list):
                for item in args[0]:
                    if item is not True:
                        return False
                return True
            return True

        if name_lower == "anytrue":
            if args and isinstance(args[0], list):
                for item in args[0]:
                    if item is True:
                        return True
                return False
            return False

        if name_lower == "allfalse":
            if args and isinstance(args[0], list):
                for item in args[0]:
                    if item is not False:
                        return False
                return True
            return True

        if name_lower == "anyfalse":
            if args and isinstance(args[0], list):
                for item in args[0]:
                    if item is False:
                        return True
                return False
            return False

        if name_lower == "reverse":
            if args and isinstance(args[0], list):
                return list(reversed(args[0]))
            return []

        if name_lower == "slice":
            if len(args) >= 3 and isinstance(args[0], list):
                start = args[1] if args[1] is not None else 0
                length = args[2] if args[2] is not None else len(args[0])
                return args[0][start : start + length]
            return []

        if name_lower == "singletonFrom":
            return self._call_builtin_function("singleton", args)

        if name_lower == "combine":
            if len(args) >= 2 and isinstance(args[0], list) and isinstance(args[1], list):
                return args[0] + args[1]
            return []

        if name_lower == "union":
            if len(args) >= 2 and isinstance(args[0], list) and isinstance(args[1], list):
                result = list(args[0])
                for item in args[1]:
                    if item not in result:
                        result.append(item)
                return result
            return []

        if name_lower == "intersect":
            if len(args) >= 2 and isinstance(args[0], list) and isinstance(args[1], list):
                return [item for item in args[0] if item in args[1]]
            return []

        if name_lower == "except":
            if len(args) >= 2 and isinstance(args[0], list) and isinstance(args[1], list):
                return [item for item in args[0] if item not in args[1]]
            return []

        # Aggregate functions with context
        if name_lower == "populationvariance":
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal))]
                if len(values) < 1:
                    return None
                mean = sum(values) / len(values)
                return sum((v - mean) ** 2 for v in values) / len(values)
            return None

        if name_lower == "variance":
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal))]
                if len(values) < 2:
                    return None
                mean = sum(values) / len(values)
                return sum((v - mean) ** 2 for v in values) / (len(values) - 1)
            return None

        if name_lower == "populationstddev":
            if args and isinstance(args[0], list):
                variance = self._call_builtin_function("populationvariance", args)
                if variance is not None:
                    return Decimal(variance).sqrt()
            return None

        if name_lower == "stddev":
            if args and isinstance(args[0], list):
                variance = self._call_builtin_function("variance", args)
                if variance is not None:
                    return Decimal(variance).sqrt()
            return None

        if name_lower == "median":
            if args and isinstance(args[0], list):
                values = sorted(v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal)))
                if not values:
                    return None
                n = len(values)
                if n % 2 == 1:
                    return values[n // 2]
                else:
                    return (values[n // 2 - 1] + values[n // 2]) / 2
            return None

        if name_lower == "mode":
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None]
                if not values:
                    return None
                # Count occurrences
                counts: dict[Any, int] = {}
                for v in values:
                    counts[v] = counts.get(v, 0) + 1
                max_count = max(counts.values())
                return [k for k, v in counts.items() if v == max_count][0]
            return None

        if name_lower == "product":
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal))]
                if not values:
                    return None
                result = Decimal(1)
                for v in values:
                    result *= Decimal(str(v))
                return result
            return None

        if name_lower == "geometricmean":
            if args and isinstance(args[0], list):
                values = [v for v in args[0] if v is not None and isinstance(v, (int, float, Decimal))]
                if not values or any(v <= 0 for v in values):
                    return None
                product = self._call_builtin_function("product", args)
                if product is not None:
                    return Decimal(product) ** (Decimal(1) / Decimal(len(values)))
            return None

        # Function not found
        return None

    # Arithmetic helpers
    def _add(self, left: Any, right: Any) -> Any:
        """Add two values."""
        if isinstance(left, Quantity) and isinstance(right, Quantity):
            if left.unit == right.unit:
                return Quantity(value=left.value + right.value, unit=left.unit)
            return None
        return left + right

    def _subtract(self, left: Any, right: Any) -> Any:
        """Subtract two values."""
        if isinstance(left, Quantity) and isinstance(right, Quantity):
            if left.unit == right.unit:
                return Quantity(value=left.value - right.value, unit=left.unit)
            return None
        return left - right

    def _multiply(self, left: Any, right: Any) -> Any:
        """Multiply two values."""
        if isinstance(left, Quantity) and isinstance(right, (int, float, Decimal)):
            return Quantity(value=left.value * Decimal(str(right)), unit=left.unit)
        if isinstance(right, Quantity) and isinstance(left, (int, float, Decimal)):
            return Quantity(value=right.value * Decimal(str(left)), unit=right.unit)
        return left * right  # type: ignore[operator]

    def _divide(self, left: Any, right: Any) -> Any:
        """Divide two values."""
        if right == 0:
            return None
        if isinstance(left, Quantity) and isinstance(right, (int, float, Decimal)):
            return Quantity(value=left.value / Decimal(str(right)), unit=left.unit)
        if isinstance(left, int) and isinstance(right, int):
            return Decimal(left) / Decimal(right)
        return left / right

    def _truncated_divide(self, left: Any, right: Any) -> int | None:
        """Truncated division (div)."""
        if right == 0:
            return None
        return int(left // right)

    def _modulo(self, left: Any, right: Any) -> Any:
        """Modulo operation."""
        if right == 0:
            return None
        return left % right

    # Three-valued logic helpers
    def _three_valued_and(self, left: Any, right: Any) -> bool | None:
        """Three-valued AND logic."""
        if left is False or right is False:
            return False
        if left is None or right is None:
            return None
        return bool(left) and bool(right)

    def _three_valued_or(self, left: Any, right: Any) -> bool | None:
        """Three-valued OR logic."""
        if left is True or right is True:
            return True
        if left is None or right is None:
            return None
        return bool(left) or bool(right)

    def _three_valued_xor(self, left: Any, right: Any) -> bool | None:
        """Three-valued XOR logic."""
        if left is None or right is None:
            return None
        return bool(left) != bool(right)

    def _three_valued_implies(self, left: Any, right: Any) -> bool | None:
        """Three-valued IMPLIES logic (left implies right)."""
        if left is False:
            return True
        if left is True and right is True:
            return True
        if left is True and right is False:
            return False
        return None

    # Equality helpers
    def _equals(self, left: Any, right: Any) -> bool | None:
        """Check equality with CQL semantics."""
        if left is None or right is None:
            return None

        # Handle lists
        if isinstance(left, list) and isinstance(right, list):
            if len(left) != len(right):
                return False
            return all(self._equals(left_item, right_item) for left_item, right_item in zip(left, right))

        # Handle Quantity
        if isinstance(left, Quantity) and isinstance(right, Quantity):
            if left.unit != right.unit:
                return None  # Incompatible units
            return left.value == right.value

        # Handle Interval
        if isinstance(left, CQLInterval) and isinstance(right, CQLInterval):
            return left == right

        # Handle Code
        if isinstance(left, CQLCode) and isinstance(right, CQLCode):
            return left.equivalent(right)

        return left == right

    # Type checking helpers
    def _check_type(self, value: Any, type_name: str) -> bool:
        """Check if value is of the given type."""
        type_lower = type_name.lower()

        if value is None:
            return False

        if type_lower in ("boolean", "system.boolean"):
            return isinstance(value, bool)
        if type_lower in ("integer", "system.integer"):
            return isinstance(value, int) and not isinstance(value, bool)
        if type_lower in ("decimal", "system.decimal"):
            return isinstance(value, Decimal | float)
        if type_lower in ("string", "system.string"):
            return isinstance(value, str)
        if type_lower in ("date", "system.date"):
            return isinstance(value, FHIRDate)
        if type_lower in ("datetime", "system.datetime"):
            return isinstance(value, FHIRDateTime)
        if type_lower in ("time", "system.time"):
            return isinstance(value, FHIRTime)
        if type_lower in ("quantity", "system.quantity"):
            return isinstance(value, Quantity)
        if type_lower in ("code", "system.code"):
            return isinstance(value, CQLCode)
        if type_lower in ("concept", "system.concept"):
            return isinstance(value, CQLConcept)

        return False

    def _cast_type(self, value: Any, type_name: str) -> Any:
        """Cast value to the given type."""
        if value is None:
            return None

        type_lower = type_name.lower()

        if type_lower in ("string", "system.string"):
            return str(value)
        if type_lower in ("integer", "system.integer"):
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        if type_lower in ("decimal", "system.decimal"):
            try:
                return Decimal(str(value))
            except (ValueError, TypeError):
                return None
        if type_lower in ("boolean", "system.boolean"):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ("true", "t", "yes", "y", "1")
            return None

        return value


del ParseTreeVisitor  # Clean up namespace
