import duckdb

from functions.init_cross_joins import init_cross_joins
from functions.init_inner_joins import init_inner_joins
from functions.init_left_joins import init_left_joins

# DuckDB connection
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# memory_state table
con.execute(
    """
    DROP TABLE IF EXISTS memory_state;
    CREATE TABLE memory_state (
        theme TEXT,
        exercise_name TEXT,
        tables JSON,
        last_reviewed DATE
    )
"""
)

# Exercise initialisation
init_cross_joins(con)
init_inner_joins(con)
init_left_joins(con)

con.close()
