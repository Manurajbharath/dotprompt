# Copyright 2025 Google LLC
# SPDX-License-Identifier: Apache-2.0

"""Custom helpers for the Handlebars template engine.

## Key helpers:

| Helper         | Description                                         |
|----------------|-----------------------------------------------------|
| `history`      | Create a dotprompt history marker.                  |
| `ifEquals`     | Compare two values and return content if equal.     |
| `json`         | Convert a value to a JSON string.                   |
| `media`        | Create a dotprompt media marker.                    |
| `role`         | Create a dotprompt role marker.                     |
| `section`      | Create a dotprompt section marker.                  |
| `unlessEquals` | Compare two values and return content unless equal. |

## Convenience functions:

| Function               | Description                               |
|------------------------|-------------------------------------------|
| `register_all_helpers` | Registers all the helpers in this module. |

"""

import json
from typing import Any

from handlebarrz import Handlebars


def json_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Convert a value to a JSON string.

    Args:
        params: List of values to convert to JSON
        hash_args: Hash arguments including formatting options.
        ctx: Current context options.

    Returns:
        JSON string representation of the value.
    """
    if not params or len(params) < 1:
        return ''

    obj = params[0]
    indent = hash_args.get('indent', 0)

    try:
        if isinstance(indent, str):
            indent = int(indent)
    except (ValueError, TypeError):
        indent = 0

    try:
        return json.dumps(obj, indent=indent)
    except (TypeError, ValueError):
        return '{}'


def role_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Create a dotprompt role marker.

    Example:

        ```handlebars
        {{role "system"}}
        ```

    Args:
        params: List of values.
        hash_args: Hash arguments.
        ctx: Current context options.

    Returns:
        Role marker of the form `<<<dotprompt:role:...>>>`.
    """
    if not params or len(params) < 1:
        return ''

    role_name = str(params[0])
    return f'<<<dotprompt:role:{role_name}>>>'


def history_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Create a dotprompt history marker.

    Example:

        ```handlebars
        {{history}}
        ```

    Args:
        params: List of values.
        hash_args: Hash arguments including formatting options.
        ctx: Current context options.

    Returns:
        History marker of the form `<<<dotprompt:history>>>`.
    """
    return '<<<dotprompt:history>>>'


def section_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Create a dotprompt section marker.

    Example:

        ```handlebars
        {{section "name"}}
        ```

    Args:
        params: List of values.
        hash_args: Hash arguments including formatting options.
        ctx: Current context options.

    Returns:
        Section marker of the form `<<<dotprompt:section ...>>>`.
    """
    if not params or len(params) < 1:
        return ''

    section_name = str(params[0])
    return f'<<<dotprompt:section {section_name}>>>'


def media_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Create a dotprompt media marker.

    Example:

        ```handlebars
        {{media url="https://example.com/image.png" contentType="image/png"}}
        ```

    Args:
        params: List of values.
        hash_args: Hash arguments including formatting options.
        ctx: Current context options.

    Returns:
        Media marker of the form `<<<dotprompt:media:url ...>>>`).
    """
    url = hash_args.get('url', '')
    if not url:
        return ''

    content_type = hash_args.get('contentType', '')
    if content_type:
        return f'<<<dotprompt:media:url {url} {content_type}>>>'
    else:
        return f'<<<dotprompt:media:url {url}>>>'

def if_equals_helper(params: list[Any], hash: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Render content if the first two parameters are equal."""
    if len(params) < 2:
        return ""

    value1, value2 = params[0], params[1]

    if value1 == value2:
        return str(ctx.get("fn", lambda: "")())  # Ensure return type is str

    return ""



def unless_equals_helper(params: list[Any], hash: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """Check if two values are not equal and render content if true."""
    if len(params) < 2:
        return ""

    value1, value2 = params[0], params[1]

    if value1 != value2:
        return ctx["fn"]() if "fn" in ctx and callable(ctx["fn"]) else ""  # Render block content

    return ""


def if_equals_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """ifEquals compares two values and returns appropriate content.

    Example:

        ```handlebars
        {{#ifEquals arg1 arg2}}
            <p>arg1 is equal to arg2</p>
        {{else}}
            <p>arg1 is not equal to arg2</p>
        {{/ifEquals}}
        ```
    Args:
        params: List containing the two values to compare.
        hash_args: Hash arguments.
        ctx: Current context options.

    Returns:
        Rendered content based on equality check.
    """
    if len(params) < 2:
        return ''

    a, b = params[0], params[1]
    fn = ctx.get('fn')
    if a == b and fn is not None:
        return str(fn(ctx))
    else:
        inverse = ctx.get('inverse')
        if inverse is not None:
            return str(inverse(ctx))
    return ''


def unless_equals_helper(
    params: list[Any], hash_args: dict[str, Any], ctx: dict[str, Any]
) -> str:
    """unlessEquals compares two values and returns appropriate content.

    Example:

        ```handlebars
        {{#unlessEquals arg1 arg2}}
            <p>arg1 is not equal to arg2</p>
        {{else}}
            <p>arg1 is equal to arg2</p>
        {{/unlessEquals}}
        ```
    Args:
        params: List containing the two values to compare.
        hash_args: Hash arguments.
        ctx: Current context options.

    Returns:
        Rendered content based on inequality check.
    """
    if len(params) < 2:
        return ''

    a, b = params[0], params[1]
    fn = ctx.get('fn')
    if a != b and fn is not None:
        return str(fn(ctx))
    else:
        inverse = ctx.get('inverse')
        if inverse is not None:
            return str(inverse(ctx))
    return ''


def register_all_helpers(handlebars: Handlebars) -> None:
    """Register all custom helpers with the handlebars instance.

    Args:
        handlebars: An instance of the Handlebars template engine.

    Returns:
        None.
    """
    handlebars.register_helper('history', history_helper)
    handlebars.register_helper('ifEquals', if_equals_helper)
    handlebars.register_helper('json', json_helper)
    handlebars.register_helper('media', media_helper)
    handlebars.register_helper('role', role_helper)
    handlebars.register_helper('section', section_helper)
    handlebars.register_helper('unlessEquals', unless_equals_helper)
