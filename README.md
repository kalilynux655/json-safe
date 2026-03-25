# json-safe

Safe JSON deserialization with type validation for Python.

## Why?

`json.loads()` happily parses anything — dicts, lists, strings, numbers. If your code
expects a dict but gets a list, you get a confusing `TypeError` deep in your logic.
Worse: attackers can exploit type confusion in deserialization to bypass validation.

`json-safe` catches this at the boundary.

## Usage

```python
from json_safe import loads_dict, loads_list, loads_safe, ValidationError

# Type-checked parsing
config = loads_dict(raw_json)       # raises if not a dict
items = loads_list(raw_json)        # raises if not a list

# With depth/size limits (prevent DoS)
data = loads_safe(raw_json, expect_type=dict, max_depth=5, max_keys=50)
```

## Install

```bash
pip install json-safe
```

## License

MIT
