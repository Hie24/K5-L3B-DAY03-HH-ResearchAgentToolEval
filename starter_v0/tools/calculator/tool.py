from __future__ import annotations

import ast
import operator
from typing import Any

from tools._shared import err

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return float(OPERATORS[op_type](left, right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return float(OPERATORS[op_type](_eval_node(node.operand)))
    else:
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def calculate(expression: str = "") -> dict[str, Any]:
    """Safely evaluates a basic mathematical arithmetic expression."""
    try:
        expr = str(expression or "").strip()
        if not expr:
            raise ValueError("Expression cannot be empty")
        parsed = ast.parse(expr, mode="eval")
        val = _eval_node(parsed.body)
        return {
            "tool": "calculate",
            "expression": expr,
            "result": int(val) if isinstance(val, float) and val.is_integer() else round(val, 6),
        }
    except Exception as exc:
        return err("calculate", exc)
