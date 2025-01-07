import duckdb

from functions.init_case_when import init_case_when
from functions.init_cross_joins import init_cross_joins
from functions.init_full_outer_joins import init_full_outer_joins
from functions.init_group_by import init_group_by
from functions.init_grouping_sets import init_grouping_sets
from functions.init_inner_joins import init_inner_joins
from functions.init_left_joins import init_left_joins
from functions.init_self_joins import init_self_joins

# DuckDB connection
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Création de la table `exercise_questions` si elle n'existe pas déjà
con.execute(
    """
    DROP TABLE IF EXISTS exercise_questions;
    CREATE TABLE exercise_questions (
    theme TEXT,
    exercise_name TEXT,
    question TEXT,
    PRIMARY KEY (theme, exercise_name)  -- Clé primaire composite
    )
    """
)

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
init_full_outer_joins(con)
init_self_joins(con)
init_group_by(con)
init_case_when(con)
init_grouping_sets(con)

con.close()
