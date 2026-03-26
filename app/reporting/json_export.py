import json
from pathlib import Path


def make_json_safe(obj):
    """
    Recursively convert objects into JSON-safe values.
    """
    if isinstance(obj, dict):
        return {key: make_json_safe(value) for key, value in obj.items()}

    if isinstance(obj, list):
        return [make_json_safe(item) for item in obj]

    if isinstance(obj, tuple):
        return [make_json_safe(item) for item in obj]

    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)


def export_report_json(report_data, output_path="outputs/report.json"):
    """
    Export the full schema analysis report to JSON.
    Creates parent directories if needed.
    """
    safe_data = make_json_safe(report_data)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(safe_data, f, indent=4)

    return output_file