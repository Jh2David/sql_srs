import json

import pandas as pd


def init_case_when(con):
    """

    :param con:
    :return:
    """

    # Wages table
    data = {
        'name': ['Toufik', 'Jean-Nicolas', 'Daniel', 'Kaouter', 'Sylvie',
                 'Sebastien', 'Diane', 'Romain', 'François', 'Anna',
                 'Zeinaba', 'Gregory', 'Karima', 'Arthur', 'Benjamin'],
        'wage': [60000, 75000, 55000, 80000, 70000,
                 90000, 65000, 72000, 68000, 85000,
                 100000, 120000, 95000, 83000, 110000],
        'department': ['IT', 'HR', 'SALES', 'IT', 'IT',
                       'HR', 'SALES', 'IT', 'HR', 'SALES',
                       'IT', 'IT', 'HR', 'SALES', 'CEO']
    }

    wages = pd.DataFrame(data)
    con.execute('CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages')

    exercises_and_questions = [
        {
            "exercise_name": "ex01_case_when_wages",
            "tables": ["wages"],
            "question": "Appliquez des augmentations à la table des salaires classé par ordre de département \n"
                        "- si le département est 'SALES' => 10% d'augmentation\n"
                        "- si le département est 'HR' => 05% d'augmentation\n"
                        "- si le département est 'IT' => 03% d'augmentation\n"
                        "- pour les autres (le CEO) => 0% d'augmentation"
        },]

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
                """,
            ("07_case_when", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
               INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
               VALUES (
                   '07_case_when',
                    '{exercise_name}',
                    '{tables}',
                    '1970-01-01'
                    )
               """
        )
