from app.metadata import get_tables, get_columns
from app.profiler import get_column_profiles, quote_identifier
from app.pk_detector import rank_pk_candidates
from app.db_connect import get_connection


def normalize_column_name(column_name: str) -> str:
    """
    Normalize column names for rough semantic comparison.
    """
    name = column_name.lower()

    if name.endswith("_id"):
        name = name[:-3]

    replacements = {
        "org": "organization",
        "acct": "account",
        "usr": "user",
        "owner": "user",
        "actor_user": "user",
    }

    return replacements.get(name, name)


def name_similarity(source_column: str, target_table: str, target_column: str) -> float:
    """
    Score whether a source column name semantically matches a target table/key.
    """
    source = normalize_column_name(source_column)
    target_table_norm = target_table.lower().rstrip("s")
    target_column_norm = normalize_column_name(target_column)

    if source == target_table_norm:
        return 1.0
    if source == target_column_norm:
        return 0.9
    if source in target_table_norm or target_table_norm in source:
        return 0.7
    return 0.0


def get_top_pk_per_table():
    """
    Return the top PK candidate for each table.
    """
    ranked = rank_pk_candidates()
    top_candidates = {}

    for table, candidates in ranked.items():
        if candidates:
            top_candidates[table] = candidates[0]

    return top_candidates


def get_subset_coverage(source_table: str, source_column: str, target_table: str, target_column: str) -> float:
    """
    Measure what fraction of distinct non-null source values exist in the target column.
    """
    source_table_q = quote_identifier(source_table)
    source_column_q = quote_identifier(source_column)
    target_table_q = quote_identifier(target_table)
    target_column_q = quote_identifier(target_column)

    query = f"""
    WITH source_vals AS (
        SELECT DISTINCT {source_column_q} AS value
        FROM {source_table_q}
        WHERE {source_column_q} IS NOT NULL
    ),
    matched AS (
        SELECT COUNT(*) AS matched_count
        FROM source_vals s
        JOIN {target_table_q} t
          ON s.value = t.{target_column_q}
    ),
    total AS (
        SELECT COUNT(*) AS total_count
        FROM source_vals
    )
    SELECT
        matched.matched_count,
        total.total_count
    FROM matched, total;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            matched_count, total_count = cur.fetchone()

    if not total_count or total_count == 0:
        return 0.0

    return round(matched_count / total_count, 3)


def infer_foreign_keys():
    """
    Infer likely FK relationships between tables.
    """
    columns = get_columns()
    profiles = get_column_profiles()
    top_pks = get_top_pk_per_table()

    profile_lookup = {
        (p["table_name"], p["column_name"]): p
        for p in profiles
    }

    results = []

    for source in columns:
        source_table = source["table_name"]
        source_column = source["column_name"]
        source_type = source["data_type"]

        # only consider columns that look like possible references
        if source_column.lower() == "id":
            continue
        if not (source_column.lower().endswith("_id") or source_type.lower() == "uuid"):
            continue

        for target_table, target_pk in top_pks.items():
            target_column = target_pk["column_name"]
            target_type = target_pk["data_type"]

            if source_table == target_table:
                continue

            type_match = 1.0 if source_type.lower() == target_type.lower() else 0.0
            if type_match == 0.0:
                continue

            subset_coverage = get_subset_coverage(
                source_table, source_column,
                target_table, target_column
            )

            semantic_score = name_similarity(source_column, target_table, target_column)
            target_pk_score = target_pk["pk_score"]

            fk_score = round(
                0.45 * subset_coverage +
                0.30 * semantic_score +
                0.25 * target_pk_score,
                3
            )

            if fk_score >= 0.5:
                results.append(
                    {
                        "source_table": source_table,
                        "source_column": source_column,
                        "target_table": target_table,
                        "target_column": target_column,
                        "fk_score": fk_score,
                        "subset_coverage": subset_coverage,
                        "semantic_score": semantic_score,
                        "target_pk_score": target_pk_score,
                    }
                )

    results.sort(key=lambda x: x["fk_score"], reverse=True)
    return results

def detect_polymorphic_patterns(columns):
    patterns = []

    table_to_columns = {}
    for col in columns:
        table_to_columns.setdefault(col["table_name"], set()).add(col["column_name"].lower())

    for table, col_names in table_to_columns.items():
        for col_name in col_names:
            if col_name.endswith("_type"):
                prefix = col_name[:-5]
                paired_id = f"{prefix}_id"
                if paired_id in col_names:
                    patterns.append({
                        "table_name": table,
                        "type_column": col_name,
                        "id_column": paired_id,
                    })

    return patterns
