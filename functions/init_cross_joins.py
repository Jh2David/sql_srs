import io
import json

import pandas as pd


def init_cross_joins(con):
    """
    Initializes the database for the "01_cross_joins" theme by creating tables and
    populating them with data. It also sets up several exercises and their questions
    related to cross joins.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
    """

    # Table des questions
    exercises_and_questions = [
        {
            "exercise_name": "beverages_and_food",
            "question": "Créez une table contenant toutes les combinaisons possibles de boissons et d'aliments, avec leurs prix respectifs.",
        },
        {
            "exercise_name": "sizes_and_trademarks",
            "question": "Créez une table contenant toutes les combinaisons possibles de tailles et de marques.",
        },
        {
            "exercise_name": "sizes_and_trademarks",
            "question": "Créez une table représentant toutes les combinaisons possibles d'heures et de quarts d'heure.",
        },
    ]

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

    # Ajoute des exercices à la table `memory_state` pour ce type de jointure
    con.execute(
        """
        INSERT INTO memory_state(theme, exercise_name, tables, last_reviewed)
        VALUES ('01_cross_joins', 'beverages_and_food', '["beverages", "food_items"]', '1970-01-01' )
    """
    )

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

    con.execute(
        """
            INSERT INTO memory_state(theme, exercise_name, tables, last_reviewed)
            VALUES ('01_cross_joins', 'sizes_and_trademarks', '["sizes", "trademarks"]', '1970-01-01' )
        """
    )

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

    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES ('01_cross_joins', 'hours_and_quarters', '["hours", "quarters"]', '1970-01-01')
    """
    )

    # Insérer les exercices et les questions
    for exercise in exercises_and_questions:
        exercise_name = exercise["exercise_name"]
        question = exercise["question"]

        # QUESTIONS
        con.execute(
            """
                    INSERT INTO exercise_questions (theme, exercise_name, question)
                    VALUES (?, ?, ?)
                """,
            ("01_cross_joins", exercise_name, question),
        )

    # ----------------------------------------------------------------------------------
    # Ajout des entrées dans memory_state
    # ----------------------------------------------------------------------------------
    exercises_and_tables = [
        {
            "exercise_name": "beverages_and_food",
            "tables": ["beverages", "food_items"],
        },
        {
            "exercise_name": "sizes_and_trademarks",
            "tables": ["sizes", "trademarks"],
        },
        {
            "exercise_name": "hours_and_quarters",
            "tables": ["hours", "quarters"],
        },
    ]

    for exercise in exercises_and_tables:
        exercise_name = exercise["exercise_name"]
        tables = json.dumps(exercise["tables"])  # Convertir la liste en chaîne JSON

        con.execute(
            """
            INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
            VALUES (?, ?, ?, ?)
            """,
            ("01_cross_joins", exercise_name, tables, "1970-01-01"),
        )
