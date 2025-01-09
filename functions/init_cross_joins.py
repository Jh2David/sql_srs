import io
import json
from datetime import date

import pandas as pd


def init_cross_joins(con):
    """
    Initializes the database for the "01_cross_joins" theme by creating tables and
    populating them with data. It also sets up several exercises and their questions
    related to cross joins.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
    """

    # ----------------------------------------------------------------------------------
    # EXERCICE 01
    # ----------------------------------------------------------------------------------
    csv = """
    beverage,price
    orange juice,2.5
    Expresso,2
    Tea,3
    """
    beverages = pd.read_csv(io.StringIO(csv))
    con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

    csv2 = """
    food_item,food_price
    cookie juice,2.5
    chocolatine,2
    muffin,3
    """
    food_items = pd.read_csv(io.StringIO(csv2))
    con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

    # ----------------------------------------------------------------------------------
    # EXERCISE 02
    # ----------------------------------------------------------------------------------
    sizes = """
    size
    XS
    M
    L
    XL
    """
    sizes = pd.read_csv(io.StringIO(sizes))
    con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

    trademarks = """
    trademark
    Nike
    Asphalte
    Abercrombie
    Lewis
    """
    trademarks = pd.read_csv(io.StringIO(trademarks))
    con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

    # ----------------------------------------------------------------------------------
    # EXERCISE 03
    # ----------------------------------------------------------------------------------
    hours = """
    hours
    8
    9
    10
    11
    12
    """
    hours = pd.read_csv(io.StringIO(hours))
    con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours")

    quarters = """
    quarter
    00
    15
    30
    45
    """
    quarters = pd.read_csv(io.StringIO(quarters))
    con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters")

    # ----------------------------------------------------------------------------------
    # Table + questions pour chaque exercice
    # ----------------------------------------------------------------------------------
    exercises_and_questions = [
        {
            "exercise_name": "beverages_and_food",
            "tables": ["beverages", "food_items"],
            "question": "Créez une table contenant toutes les combinaisons possibles de boissons et d'aliments, avec leurs prix respectifs.",
        },
        {
            "exercise_name": "sizes_and_trademarks",
            "tables": ["sizes", "trademarks"],
            "question": "Créez une table contenant toutes les combinaisons possibles de tailles et de marques.",
        },
        {
            "exercise_name": "hours_and_quarters",
            "tables": ["hours", "quarters"],
            "question": "Créez une table représentant toutes les combinaisons possibles d'heures et de quarts d'heure.",
        },
    ]

    # Insérer les exercices et les questions
    for exercise in exercises_and_questions:
        exercise_name = exercise["exercise_name"]
        tables = json.dumps(exercise["tables"])
        question = exercise["question"]

        # QUESTIONS
        con.execute(
            """
                    INSERT INTO exercise_questions (theme, exercise_name, question)
                    VALUES (?, ?, ?)
                    ON CONFLICT (theme, exercise_name) DO NOTHING;
                """,
            ("01_cross_joins", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
                INSERT OR IGNORE INTO memory_state (theme, exercise_name, tables, last_reviewed)
                VALUES (
                    '01_cross_joins',
                    '{exercise_name}',
                    '{tables}',
                    '{date.today()}'
                    )
            """
        )
