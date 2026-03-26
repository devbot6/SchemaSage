from app.db_connect import get_connection


def get_tables():
    """
    Return a list of table names from the public schema.
    """
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [row[0] for row in rows]


def get_columns():
    """
    Return column metadata for all tables in the public schema.
    """
    query = """
    SELECT
        table_name,
        column_name,
        data_type,
        is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    columns = []
    for row in rows:
        columns.append(
            {
                "table_name": row[0],
                "column_name": row[1],
                "data_type": row[2],
                "is_nullable": row[3],
            }
        )

    return columns