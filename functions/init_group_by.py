import pandas as pd


def init_group_by(con):
    """
    Initializes the database for the "06_group_by" theme by creating a table and populating
    it with data from a CSV file. It also sets up several exercises related to the theme.

    Steps performed:
    1. Loads the `appartements_nord_pdc.csv` file into a Pandas DataFrame.
    2. Creates the `appt_nord` table in the database if it doesn't already exist and populates it with the DataFrame data.
    3. Inserts exercise definitions into the `memory_state` table for various GROUP BY-related exercises.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
    """
    appt_nord = pd.read_csv("data/06_group_by/appartements_nord_pdc.csv")
    con.execute("CREATE TABLE IF NOT EXISTS appt_nord AS SELECT * FROM appt_nord")

    # Table des questions
    con.execute(
        """
            CREATE TABLE IF NOT EXISTS exercise_questions (
                theme TEXT,
                exercise_name TEXT,
                question TEXT
            )
        """
    )

    exercises_and_questions = [
        {
            "exercise_name": "ex01_group_by_appt_nord",
            "question": "Combien de ventes ont été réalisées par commune ?",
        },
        {
            "exercise_name": "ex02_group_by_appt_nord",
            "question": "Quelle est la moyenne des prix par commune ?",
        },
        {
            "exercise_name": "ex03_group_by_appt_nord",
            "question": "Quelle est la moyenne des prix par commune et le nombre de logements associé (nb_lines) ?",
        },
        {
            "exercise_name": "ex04_where_and_subquery_appt_nord",
            "question": "Appliquez une clause WHERE et une subquery pour sélectionner les communes proposant plus de 10 logements (nb_lines>10) .",
        },
        {
            "exercise_name": "ex05_where_and_CTE_appt_nord",
            "question": "Utilisez une CTE pour sélectionner les communes proposant plus de 10 logements (nb_lines>10)",
        },
        {
            "exercise_name": "ex06_where_and_having_appt_nord",
            "question": "Utiliser une clause HAVING pour filtrer les communes proposant plus de 10 logements (nb_lines>10)",
        },
    ]

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
            ("06_group_by", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
            INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
            VALUES (
                '06_group_by',
                 '{exercise_name}',
                 '["appt_nord"]',
                 '1970-01-01'
                 )
            """
        )
