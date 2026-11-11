from __future__ import annotations

import ast
import math
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


def _checked(value: int | float) -> int | float:
    if type(value) not in (int, float):
        raise ValueError("Only real numbers are supported")
    if isinstance(value, int) and value.bit_length() > 4096:
        raise ValueError("Integer result is too large")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Result must be finite")
    return value


def _eval_node(node: ast.AST) -> int | float:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return _checked(node.value)
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Pow:
            if abs(right) > 1000:
                raise ValueError("Exponent is too large")
            if isinstance(left, int) and isinstance(right, int) and right > 0 and left.bit_length() * right > 4096:
                raise ValueError("Power result is too large")
        return _checked(OPERATORS[op_type](left, right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _checked(OPERATORS[op_type](_eval_node(node.operand)))
    else:
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def calculate(expression: str = "") -> dict[str, Any]:
    """Safely evaluates a basic mathematical arithmetic expression."""
    try:
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string")
        expr = expression.strip()
        if not expr:
            raise ValueError("Expression cannot be empty")
        if len(expr) > 512:
            raise ValueError("Expression is too long")
        parsed = ast.parse(expr, mode="eval")
        if sum(1 for _ in ast.walk(parsed)) > 128:
            raise ValueError("Expression is too complex")
        val = _eval_node(parsed.body)
        return {
            "tool": "calculate",
            "expression": expr,
            "result": val if isinstance(val, int) else (int(val) if val.is_integer() else round(val, 6)),
        }
    except Exception as exc:
        return err("calculate", exc)
