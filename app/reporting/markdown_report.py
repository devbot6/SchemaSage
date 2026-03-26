from pathlib import Path


def generate_markdown_report(report_data, output_path="outputs/report.md"):
    """
    Generate a human-readable Markdown report.
    Expects categorized finding groups in report_data.
    Creates parent directories if needed.
    """
    lines = []
    lines.append("# SchemaSage Report")
    lines.append("")

    lines.append("## Tables")
    for table in report_data["tables"]:
        lines.append(f"- {table}")
    lines.append("")

    lines.append("## Likely Primary Keys")
    pk_candidates = report_data["pk_candidates"]
    for table, candidates in pk_candidates.items():
        lines.append(f"### {table}")
        for candidate in candidates[:3]:
            lines.append(
                f"- `{candidate['column_name']}` "
                f"(score={candidate['pk_score']}, "
                f"type={candidate['data_type']}, "
                f"distinct_ratio={candidate['distinct_ratio']}, "
                f"null_ratio={candidate['null_ratio']})"
            )
        lines.append("")

    lines.append("## Likely Foreign Keys")
    clean_fks = report_data.get("clean_foreign_keys", [])
    if clean_fks:
        for fk in clean_fks:
            lines.append(
                f"- `{fk['source_table']}.{fk['source_column']}` -> "
                f"`{fk['target_table']}.{fk['target_column']}` "
                f"(score={fk['fk_score']}, "
                f"coverage={fk['subset_coverage']}, "
                f"name_score={fk['semantic_score']}, "
                f"target_pk_score={fk['target_pk_score']})"
            )
    else:
        lines.append("- None detected")
    lines.append("")

    lines.append("## Suspicious / Orphan References")
    suspicious_fks = report_data.get("suspicious_references", [])
    if suspicious_fks:
        for fk in suspicious_fks:
            lines.append(
                f"- `{fk['source_table']}.{fk['source_column']}` -> "
                f"`{fk['target_table']}.{fk['target_column']}` "
                f"(score={fk['fk_score']}; partial coverage={fk['subset_coverage']})"
            )
    else:
        lines.append("- None detected")
    lines.append("")

    lines.append("## Ambiguous References")
    ambiguous_fks = report_data.get("ambiguous_references", [])
    if ambiguous_fks:
        for fk in ambiguous_fks:
            reason_parts = []

            if "subset_coverage" in fk:
                reason_parts.append(f"partial coverage={fk['subset_coverage']}")

            if fk.get("is_polymorphic", False):
                reason_parts.append("polymorphic reference pattern")

            reason_text = ", ".join(reason_parts) if reason_parts else "heuristic uncertainty"

            lines.append(
                f"- `{fk['source_table']}.{fk['source_column']}` -> "
                f"`{fk['target_table']}.{fk['target_column']}` "
                f"(score={fk['fk_score']}; {reason_text})"
            )
    else:
        lines.append("- None detected")
    lines.append("")

    lines.append("## Polymorphic Reference Patterns")
    polymorphic_patterns = report_data.get("polymorphic_patterns", [])
    if polymorphic_patterns:
        for pattern in polymorphic_patterns:
            lines.append(
                f"- `{pattern['table_name']}.{pattern['type_column']}` + "
                f"`{pattern['table_name']}.{pattern['id_column']}`"
            )
    else:
        lines.append("- None detected")
    lines.append("")

    lines.append("## Notes")
    lines.append("- Inference is heuristic and confidence-scored.")
    lines.append("- Small datasets can make non-key columns appear artificially unique.")
    lines.append("- Reference-style columns ending in `_id` are not necessarily table primary keys.")
    lines.append("- Suspicious / orphan references indicate likely FK intent with incomplete referential coverage.")
    lines.append("- Polymorphic references may not map cleanly to a single foreign key.")
    lines.append("")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_file