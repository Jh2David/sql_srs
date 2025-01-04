import json

import pandas as pd


def init_case_when(con):
    """

    :param con:
    :return:
    """

    # Wages table
    data = {
        "name": [
            "Toufik",
            "Jean-Nicolas",
            "Daniel",
            "Kaouter",
            "Sylvie",
            "Sebastien",
            "Diane",
            "Romain",
            "François",
            "Anna",
            "Zeinaba",
            "Gregory",
            "Karima",
            "Arthur",
            "Benjamin",
        ],
        "wage": [
            60000,
            75000,
            55000,
            80000,
            70000,
            90000,
            65000,
            72000,
            68000,
            85000,
            100000,
            120000,
            95000,
            83000,
            110000,
        ],
        "department": [
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "CEO",
        ],
    }

    wages = pd.DataFrame(data)
    con.execute("CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages")

    # Products store
    data = {
        "order_id": [1, 2, 3, 4, 5, 6],
        "product_id": [101, 102, 101, 103, 102, 103],
        "quantity": [5, 3, 2, 4, 6, 2],
        "price_per_unit": [10.0, 25.0, 10.0, 8.0, 25.0, 8.0],
        "discount_code": [None, "DISCOUNT10", "DISCOUNT20", None, None, "UNKNOWN"],
    }
    df = pd.DataFrame(data)
    con.execute("CREATE TABLE IF NOT EXISTS df AS SELECT * FROM df")

    exercises_and_questions = [
        {
            "exercise_name": "ex01A_case_when_wages",
            "tables": ["wages"],
            "question": "Appliquez des augmentations à la table des salaires classé par ordre de département \n"
            "- si le département est 'SALES' => 10% d'augmentation\n"
            "- si le département est 'HR' => 05% d'augmentation\n"
            "- si le département est 'IT' => 03% d'augmentation\n"
            "- pour les autres (le CEO) => 0% d'augmentation",
        },
        {
            "exercise_name": "ex02A_case_when_products",
            "tables": ["df"],
            "question": "Calculer la somme des ventes après réduction (CTE)\n"
            "- Faites une CTE avec le CASE WHEN dedans (la colonne crée par le CASE WHEN s'appelle 'total_revenue'\n"
            "- Utilisez cette table intermédiaire pour calculer le revenu total une fois les réductions déduites",
        },
        {
            "exercise_name": "ex02B_case_when_products",
            "tables": ["df"],
            "question": "Calculer la somme des ventes après réduction (1 seule query)\n"
            "Essayez de tout faire en une seule requête, en 'englobant' votre case when par un 'SUM()'"
            "et trier par le total_revenue",
        },
        {
            "exercise_name": "ex01B_case_when_wages",
            "tables": ["wages"],
            "question": "Classer les revenus par catégories trié par l'average_salary \n"
            "Il est possible de faire des CASE WHEN à l'intérieur de la clause GROUP BY:\n"
            "- Low si < 50 000\n"
            "- medium si < 90 000\n"
            "- sinon: high"
            "Info: les CASE WHEN dans les GROUP BY ne sont pas la solution la plus facile à maintenir, les"
            "CTE conviennent mieux pour ce type de besoin",
        },
        {
            "exercise_name": "ex01C_case_when_wages",
            "tables": ["wages"],
            "question": "Classer les revenus par catégories trié par l'average_salary \n"
            "Refaites l/'exercice 01B en utilisant une CTE qui crée la colonne 'salary_range' avec un CASE"
            "WHEN. Puis en faisant la moyenne des salaires par salary_range\n"
            "- Low si < 50 000\n"
            "- medium si < 90 000\n"
            "- sinon: high",
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
