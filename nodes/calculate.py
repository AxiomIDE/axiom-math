from gen.messages_pb2 import MathRequest, MathResult
from gen.axiom_context import AxiomContext


# Maps every accepted spelling of an operation to a canonical name.
_ALIASES = {
    "add": "add", "+": "add", "plus": "add", "sum": "add",
    "subtract": "subtract", "sub": "subtract", "-": "subtract", "minus": "subtract",
    "multiply": "multiply", "mul": "multiply", "*": "multiply", "x": "multiply", "times": "multiply",
    "divide": "divide", "div": "divide", "/": "divide",
    "power": "power", "pow": "power", "^": "power", "**": "power",
    "modulo": "modulo", "mod": "modulo", "%": "modulo",
}


def calculate(ax: AxiomContext, input: MathRequest) -> MathResult:
    """Perform a binary arithmetic operation on two operands.

    Supports add, subtract, multiply, divide, power and modulo. The operation
    name is case-insensitive and accepts common aliases (+, -, *, /, ^, %).
    Returns the numeric result, or an `error` message on an unknown operation
    or a divide/modulo by zero.
    """
    op = _ALIASES.get(input.operation.strip().lower())
    a, b = input.a, input.b

    if op is None:
        ax.log.warn("unknown operation", operation=input.operation)
        return MathResult(
            error=f"unknown operation: {input.operation!r}",
            operation=input.operation,
        )

    if op in ("divide", "modulo") and b == 0:
        return MathResult(error=f"cannot {op} by zero", operation=op)

    if op == "add":
        value = a + b
    elif op == "subtract":
        value = a - b
    elif op == "multiply":
        value = a * b
    elif op == "divide":
        value = a / b
    elif op == "power":
        value = a ** b
    else:  # modulo
        value = a % b

    ax.log.info("calculated", operation=op, a=a, b=b, value=value)
    return MathResult(value=value, operation=op)
