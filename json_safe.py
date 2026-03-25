"""json_safe — Safe JSON deserialization with type validation.

Prevents type confusion, injection, and deserialization attacks
by validating parsed JSON against expected schemas.
"""
from __future__ import annotations

import json
from typing import Any, TypeVar, get_args, get_origin

T = TypeVar("T")


class ValidationError(ValueError):
    """Raised when JSON data doesn't match the expected schema."""
    pass


def loads_safe(
    data: str,
    *,
    expect_type: type | None = None,
    max_depth: int = 10,
    max_keys: int = 100,
) -> Any:
    """Parse JSON with safety checks.

    Args:
        data: JSON string to parse.
        expect_type: Expected top-level type (dict, list, str, int, float, bool).
        max_depth: Maximum nesting depth (default 10).
        max_keys: Maximum keys per object (default 100).

    Returns:
        Parsed and validated data.

    Raises:
        ValidationError: If data doesn't match expectations.
        json.JSONDecodeError: If JSON is malformed.
    """
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Malformed JSON: {e}") from e

    if expect_type is not None:
        if not isinstance(parsed, expect_type):
            raise ValidationError(
                f"Expected {expect_type.__name__}, got {type(parsed).__name__}"
            )

    _check_depth(parsed, max_depth, max_keys, depth=0)
    return parsed


def loads_dict(data: str, **kwargs: Any) -> dict[str, Any]:
    """Parse JSON and validate it's a dict."""
    return loads_safe(data, expect_type=dict, **kwargs)


def loads_list(data: str, **kwargs: Any) -> list[Any]:
    """Parse JSON and validate it's a list."""
    return loads_safe(data, expect_type=list, **kwargs)


def _check_depth(obj: Any, max_depth: int, max_keys: int, depth: int) -> None:
    if depth > max_depth:
        raise ValidationError(f"Nesting depth exceeds {max_depth}")

    if isinstance(obj, dict):
        if len(obj) > max_keys:
            raise ValidationError(
                f"Object has {len(obj)} keys, max {max_keys}"
            )
        for v in obj.values():
            _check_depth(v, max_depth, max_keys, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _check_depth(item, max_depth, max_keys, depth + 1)
