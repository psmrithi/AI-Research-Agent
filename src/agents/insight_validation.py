import re


NUMBER_PATTERN = re.compile(r"-?\d[\d,]*\.?\d*")


def extract_numbers(text):
    """Pull every number out of a piece of text."""
    numbers = []

    for match in NUMBER_PATTERN.findall(text or ""):
        cleaned = match.replace(",", "")

        try:
            numbers.append(float(cleaned))
        except ValueError:
            continue

    return numbers


def collect_allowed_numbers(data_stats=None, research_summary=None):
    """Build the pool of numbers an insight is allowed to mention."""

    allowed = set()

    if data_stats:
        for col_stats in data_stats.values():
            for key in ("mean", "median", "std", "min", "max"):
                value = col_stats.get(key)

                if value is not None:
                    allowed.add(round(float(value), 3))

    if research_summary:
        blobs = (
            [research_summary.overview or ""]
            + [c.statement for c in research_summary.claims]
        )

        for blob in blobs:
            for number in extract_numbers(blob):
                allowed.add(round(number, 3))

    return allowed


def is_number_supported(
    number,
    allowed_numbers,
    rel_tol=0.02,
    abs_tol=0.5,
):
    """Check whether a number is close to a real calculated value."""

    for allowed in allowed_numbers:
        if abs(number - allowed) <= max(
            abs_tol,
            rel_tol * abs(allowed),
        ):
            return True

    return False


def validate_insight(text, allowed_numbers):
    """Return whether an insight contains only supported numbers."""

    numbers = extract_numbers(text)

    unsupported = [
        number
        for number in numbers
        if not is_number_supported(number, allowed_numbers)
    ]

    return len(unsupported) == 0, unsupported