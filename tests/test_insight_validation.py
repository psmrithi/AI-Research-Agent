from src.agents.insight_validation import (
    collect_allowed_numbers,
    extract_numbers,
    is_number_supported,
    validate_insight,
)


def test_extract_numbers_handles_commas_and_percent():
    assert extract_numbers("Sales rose to 1,234.5 units, up 12%.") == [1234.5, 12.0]


def test_extract_numbers_empty_text():
    assert extract_numbers("") == []
    assert extract_numbers(None) == []


def test_is_number_supported_within_tolerance():
    assert is_number_supported(14.9, {14.87}) is True


def test_is_number_supported_rejects_far_off_value():
    assert is_number_supported(500, {14.87}) is False


def test_collect_allowed_numbers_from_stats_and_claims():
    stats = {"price": {"mean": 12.5, "min": 9.0, "max": 16.0}}

    class FakeClaim:
        statement = "Registrations reached 2.1 million in 2023."

    class FakeSummary:
        overview = "Overview text."
        claims = [FakeClaim()]

    allowed = collect_allowed_numbers(stats, FakeSummary())
    assert 12.5 in allowed and 2.1 in allowed and 2023 in allowed


def test_validate_insight_flags_invented_number():
    ok, unsupported = validate_insight(
        "Prices averaged 999.9 lakh.",
        {12.5},
    )
    assert ok is False
    assert 999.9 in unsupported


def test_validate_insight_allows_grounded_number():
    ok, unsupported = validate_insight(
        "Average price was 12.5 lakh.",
        {12.5},
    )
    assert ok is True
    assert unsupported == []