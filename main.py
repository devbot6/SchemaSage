from app.metadata import get_tables, get_columns
from app.profiler import get_column_profiles
from app.pk_detector import rank_pk_candidates
from app.fk_detector import infer_foreign_keys, detect_polymorphic_patterns
from app.reporting.json_export import export_report_json
from app.reporting.markdown_report import generate_markdown_report


def categorize_fk_findings(fk_candidates, polymorphic_patterns):
    """
    Split FK candidates into clean, suspicious/orphan, and ambiguous groups.
    """
    polymorphic_pairs = {
        (pattern["table_name"], pattern["id_column"])
        for pattern in polymorphic_patterns
    }

    clean_fks = []
    suspicious_fks = []
    ambiguous_fks = []

    for fk in fk_candidates:
        is_polymorphic = (fk["source_table"], fk["source_column"]) in polymorphic_pairs
        coverage = fk["subset_coverage"]

        if is_polymorphic:
            fk_copy = dict(fk)
            fk_copy["is_polymorphic"] = True
            ambiguous_fks.append(fk_copy)
        elif coverage < 0.95:
            suspicious_fks.append(fk)
        else:
            clean_fks.append(fk)

    return clean_fks, suspicious_fks, ambiguous_fks


def main():
    tables = get_tables()
    columns = get_columns()
    profiles = get_column_profiles()
    pk_candidates = rank_pk_candidates()
    fk_candidates = infer_foreign_keys()
    polymorphic_patterns = detect_polymorphic_patterns(columns)

    clean_fks, suspicious_fks, ambiguous_fks = categorize_fk_findings(
        fk_candidates,
        polymorphic_patterns
    )

    report_data = {
        "tables": tables,
        "columns": columns,
        "column_profiles": profiles,
        "pk_candidates": pk_candidates,
        "fk_candidates": fk_candidates,
        "clean_foreign_keys": clean_fks,
        "suspicious_references": suspicious_fks,
        "ambiguous_references": ambiguous_fks,
        "polymorphic_patterns": polymorphic_patterns,
    }

    json_file = export_report_json(report_data, "outputs/report.json")
    markdown_file = generate_markdown_report(report_data, "outputs/report.md")

    print("\nSchemaSage analysis complete.")
    print(f"JSON report written to: {json_file}")
    print(f"Markdown report written to: {markdown_file}")

    print("\nTop likely foreign keys:")
    if clean_fks:
        for fk in clean_fks[:5]:
            print(
                f"- {fk['source_table']}.{fk['source_column']} -> "
                f"{fk['target_table']}.{fk['target_column']} "
                f"(score={fk['fk_score']})"
            )
    else:
        print("- None detected")

    print("\nSuspicious / orphan references:")
    if suspicious_fks:
        for fk in suspicious_fks[:5]:
            print(
                f"- {fk['source_table']}.{fk['source_column']} -> "
                f"{fk['target_table']}.{fk['target_column']} "
                f"(coverage={fk['subset_coverage']}, score={fk['fk_score']})"
            )
    else:
        print("- None detected")

    print("\nPolymorphic patterns:")
    if polymorphic_patterns:
        for pattern in polymorphic_patterns:
            print(
                f"- {pattern['table_name']}: "
                f"{pattern['type_column']} + {pattern['id_column']}"
            )
    else:
        print("- None detected")


if __name__ == "__main__":
    main()