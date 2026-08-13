"""
priority.py

Priority is calculated using a simple impact/urgency matrix inspired by
common IT service management (ITIL) practices. In a real organization,
the exact matrix would be defined by the organization's policies.
"""

# Impact/Urgency -> Priority matrix
PRIORITY_MATRIX = {
    ("High", "High"): "Critical",
    ("High", "Medium"): "High",
    ("High", "Low"): "Medium",
    ("Medium", "High"): "High",
    ("Medium", "Medium"): "Medium",
    ("Medium", "Low"): "Low",
    ("Low", "High"): "Medium",
    ("Low", "Medium"): "Low",
    ("Low", "Low"): "Low",
}

VALID_LEVELS = ("Low", "Medium", "High")


def calculate_priority(impact: str, urgency: str) -> str:
    """
    Calculate ticket priority from impact and urgency.

    Args:
        impact: 'Low', 'Medium', or 'High'
        urgency: 'Low', 'Medium', or 'High'

    Returns:
        Priority string: 'Low', 'Medium', 'High', or 'Critical'

    Raises:
        ValueError: if impact or urgency is not a recognized value.
    """
    if impact not in VALID_LEVELS or urgency not in VALID_LEVELS:
        raise ValueError(
            f"Impact and urgency must be one of {VALID_LEVELS}, "
            f"got impact={impact!r}, urgency={urgency!r}"
        )
    return PRIORITY_MATRIX[(impact, urgency)]
