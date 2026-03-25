"""Tests for json_safe."""
import pytest
from json_safe import loads_safe, loads_dict, loads_list, ValidationError


class TestLoadsSafe:
    def test_valid_dict(self):
        result = loads_safe('{"key": "value"}', expect_type=dict)
        assert result == {"key": "value"}

    def test_valid_list(self):
        result = loads_safe('[1, 2, 3]', expect_type=list)
        assert result == [1, 2, 3]

    def test_type_mismatch(self):
        with pytest.raises(ValidationError, match="Expected dict"):
            loads_safe('[1, 2]', expect_type=dict)

    def test_malformed_json(self):
        with pytest.raises(ValidationError, match="Malformed JSON"):
            loads_safe("{bad json")

    def test_max_depth(self):
        nested = '{"a": {"b": {"c": {"d": "deep"}}}}'
        loads_safe(nested, max_depth=5)  # OK
        with pytest.raises(ValidationError, match="Nesting depth"):
            loads_safe(nested, max_depth=2)

    def test_max_keys(self):
        many_keys = "{" + ", ".join(f'"k{i}": {i}' for i in range(50)) + "}"
        with pytest.raises(ValidationError, match="keys"):
            loads_safe(many_keys, max_keys=10)


class TestConvenienceFunctions:
    def test_loads_dict(self):
        assert loads_dict('{"a": 1}') == {"a": 1}

    def test_loads_list(self):
        assert loads_list('[1, 2]') == [1, 2]

    def test_loads_dict_rejects_list(self):
        with pytest.raises(ValidationError):
            loads_dict('[1, 2]')
