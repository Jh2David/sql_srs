import json
from datetime import date

import pandas as pd


def init_case_when(con):
    """
    Initializes the database for the "07_case_when" theme by creating tables and
    populating them with data. It also sets up several exercises and their questions
    related to the usage of the CASE WHEN statement in SQL queries.

    This function performs the following tasks:
    1. Creates tables for wage data, product sales data, and football match data.
    2. Inserts various exercises and their associated questions into the `exercise_questions`
       and `memory_state` tables to be used for practicing SQL queries with CASE WHEN logic.
    3. The exercises cover topics such as salary adjustments, calculating total revenue with discounts,
       and analyzing football match results using conditional statements.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
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

    # Foot Table

    df_foot = pd.read_csv("data/07_case_when/season_1011.csv")
    con.execute("CREATE TABLE IF NOT EXISTS df_foot AS SELECT * FROM df_foot")

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
            "Refaites l'exercice 01B en utilisant une CTE qui crée la colonne 'salary_range' avec un CASE"
            "WHEN. Puis en faisant la moyenne des salaires par salary_range\n"
            "- Low si < 50 000\n"
            "- medium si < 90 000\n"
            "- sinon: high",
        },
        {
            "exercise_name": "ex03A_case_when_football",
            "tables": ["df_foot"],
            "question": "Combien de Match Lille a gagné?\n"
            "- A domicile\n"
            "- A l'extérieur\n\n"
            "Pour déterminer que Lille a gagné à domicile, il faut que:\n"
            "- La HomeTeam soit Lille\n"
            "- FTHG (pour Full Time Home Goal) soit supérieur à FTAG (Full Time Away Goal: nombre de goal "
            "scorés par la 'AwayTeam')\n"
            "- Pour faciliter l'exercice, on ne prend pas le cas de figure où il y a match nul à la 90' "
            "minute et qu'un but est inscrit pendant le temps additionnel\n\n"
            "Exercice:\n"
            "- Utilisez un CASE WHEN pour recenser les cas de figure où lille gagne à domicile"
            "(en utilisant la règle ci-dessus)\n"
            "- Englobez ce CASE WHEN dans un count pour compter le total de victoire à domicile\n"
            "- Faites la même chose avec les matchs à l'extérieur\n\n"
            "Hint: pour faire le count, il faut grouper sur quelque chose. "
            "Utilisez 'Div': on veut les matchs gagnés en L1.",
        },
        {
            "exercise_name": "ex03B_case_when_football",
            "tables": ["df_foot"],
            "question": "On a gagné 13 matchs sur combien?\n"
            "Comment faire pour ne pas prendre en compte tous ces matchs qui ne concernent pas Lille?\n\n"
            "Attention :\n"
            "L'utilisation du ELSE pourrai-être une solution, cependant il faut bien choisir "
            "où mettre des 0. "
            "Comment pourrait-on procéder pour n'avoir de 0 que quand le match concerne "
            "Lille (et que Lille a perdu)?",
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
               INSERT OR IGNORE INTO memory_state (theme, exercise_name, tables, last_reviewed)
               VALUES (
                   '07_case_when',
                    '{exercise_name}',
                    '{tables}',
                    '{date.today()}'
                    )
               """
        )
