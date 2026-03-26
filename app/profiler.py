from app.db_connect import get_connection
from app.metadata import get_tables, get_columns

def quote_identifier(name: str) -> str:
    """
    Safely quote a SQL identifier like a table or column name.
    """
    return '"' + name.replace('"', '""') + '"'


def get_column_profiles():
    """
    Profile every column in every public table.
    Returns a list of dictionaries with summary statistics.
    """
    tables = get_tables()
    columns = get_columns()

    profiles = []

    with get_connection() as conn:
        with conn.cursor() as cur:
            for table in tables:
                table_columns = [col for col in columns if col["table_name"] == table]

                for col in table_columns:
                    table_name = quote_identifier(table)
                    column_name = quote_identifier(col["column_name"])

                    query = f"""
                    SELECT
                        COUNT(*) AS total_rows,
                        COUNT(*) FILTER (WHERE {column_name} IS NULL) AS null_count,
                        COUNT(DISTINCT {column_name}) AS distinct_count
                    FROM {table_name};
                    """

                    cur.execute(query)
                    result = cur.fetchone()

                    total_rows = result[0] or 0
                    null_count = result[1] or 0
                    distinct_count = result[2] or 0

                    null_ratio = (null_count / total_rows) if total_rows > 0 else 0
                    distinct_ratio = (distinct_count / total_rows) if total_rows > 0 else 0

                    sample_query = f"""
                    SELECT {column_name}
                    FROM {table_name}
                    WHERE {column_name} IS NOT NULL
                    LIMIT 5;
                    """

                    cur.execute(sample_query)
                    sample_rows = cur.fetchall()
                    sample_values = [row[0] for row in sample_rows]

                    profiles.append(
                        {
                            "table_name": table,
                            "column_name": col["column_name"],
                            "data_type": col["data_type"],
                            "is_nullable": col["is_nullable"],
                            "total_rows": total_rows,
                            "null_count": null_count,
                            "null_ratio": round(null_ratio, 3),
                            "distinct_count": distinct_count,
                            "distinct_ratio": round(distinct_ratio, 3),
                            "sample_values": sample_values,
                        }
                    )

    return profiles