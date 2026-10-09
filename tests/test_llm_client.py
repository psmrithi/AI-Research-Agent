import pytest
from pydantic import BaseModel

from src.llm.client import parse_json_response


class Demo(BaseModel):
    name: str
    year: int


def test_clean_json():
    result = parse_json_response(
        '{"name": "Bitcoin", "year": 2022}',
        Demo,
    )

    assert result.name == "Bitcoin"
    assert result.year == 2022


def test_markdown_fences():
    result = parse_json_response(
        '```json\n{"name": "Bitcoin", "year": 2022}\n```',
        Demo,
    )

    assert result.name == "Bitcoin"
    assert result.year == 2022


def test_wrong_type_raises():
    with pytest.raises(ValueError):
        parse_json_response(
            '{"name": "Bitcoin", "year": "wrong"}',
            Demo,
        )


def test_missing_field_raises():
    with pytest.raises(ValueError):
        parse_json_response(
            '{"name": "Bitcoin"}',
            Demo,
        )


def test_invalid_json_raises():
    with pytest.raises(ValueError):
        parse_json_response(
            '{"name": "Bitcoin", "year": }',
            Demo,
        )