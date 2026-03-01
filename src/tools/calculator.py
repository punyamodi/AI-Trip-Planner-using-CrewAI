import ast
import operator
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


class CalculatorInput(BaseModel):
    expression: str = Field(
        description="A mathematical expression to evaluate, e.g. '200 * 7' or '(500 + 300) / 4'"
    )


class CalculatorTool(BaseTool):
    name: str = "Calculate"
    description: str = (
        "Evaluates mathematical expressions for budget calculations and cost estimates. "
        "Input should be a valid math expression such as '200 * 7' or '(1200 + 800) * 2'."
    )
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            tree = ast.parse(expression.strip(), mode="eval")
            result = self._evaluate(tree.body)
            return str(round(float(result), 2))
        except ZeroDivisionError:
            return "Error: Division by zero"
        except (ValueError, TypeError, SyntaxError) as exc:
            return f"Calculation error: {exc}"

    def _evaluate(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            return SAFE_OPERATORS[op_type](left, right)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._evaluate(node.operand)
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
