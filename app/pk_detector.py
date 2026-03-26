from app.profiler import get_column_profiles


def score_name(column_name: str) -> float:
    """
    Score how much the column name looks like a primary key.
    """
    name = column_name.lower()

    if name == "id":
        return 1.0
    if name in {"uuid", "pk"}:
        return 0.8
    if name.endswith("_id"):
        return 0.25
    return 0.0

def reference_penalty(column_name: str) -> float:
    """
    Penalize columns that look like foreign-key/reference fields rather than PKs.
    """
    name = column_name.lower()

    if name != "id" and name.endswith("_id"):
        return 1.0
    return 0.0


def score_type(data_type: str) -> float:
    """
    Score how much the data type looks like a primary key type.
    """
    dtype = data_type.lower()

    if "uuid" in dtype:
        return 1.0
    if "integer" in dtype or "bigint" in dtype or "smallint" in dtype:
        return 0.8
    if "text" in dtype or "character" in dtype:
        return 0.3
    return 0.1


def penalty_name(column_name: str) -> float:
    """
    Penalize columns whose names usually describe attributes, not identifiers.
    """
    name = column_name.lower()

    penalty_terms = {
        "name", "full_name", "email", "status", "action",
        "industry", "created_at", "updated_at", "issued_at",
        "paid_at", "started_at", "target_type", "amount_cents"
    }

    return 1.0 if name in penalty_terms else 0.0


def calculate_pk_score(profile: dict) -> float:
    """
    Calculate a weighted PK score for a column profile.
    """
    distinct_ratio = profile["distinct_ratio"]
    null_ratio = profile["null_ratio"]
    non_null_score = 1.0 - null_ratio
    name_score = score_name(profile["column_name"])
    type_score = score_type(profile["data_type"])
    descriptive_penalty = penalty_name(profile["column_name"])
    ref_penalty = reference_penalty(profile["column_name"])

    score = (
        0.40 * distinct_ratio +
        0.30 * non_null_score +
        0.20 * name_score +
        0.10 * type_score
    ) - (0.25 * descriptive_penalty) - (0.30 * ref_penalty)

    return round(max(score, 0.0), 3)

def rank_pk_candidates():
    """
    Rank PK candidates for each table.
    Returns a dictionary:
    {
        "table_name": [
            {"column_name": ..., "pk_score": ...},
            ...
        ]
    }
    """
    profiles = get_column_profiles()
    results = {}

    for profile in profiles:
        table = profile["table_name"]
        score = calculate_pk_score(profile)

        candidate = {
            "column_name": profile["column_name"],
            "data_type": profile["data_type"],
            "pk_score": score,
            "distinct_ratio": profile["distinct_ratio"],
            "null_ratio": profile["null_ratio"],
        }

        if table not in results:
            results[table] = []

        results[table].append(candidate)

    for table in results:
        results[table].sort(key=lambda x: x["pk_score"], reverse=True)

    return results