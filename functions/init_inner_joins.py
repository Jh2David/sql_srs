import json
from datetime import date

import pandas as pd


def init_inner_joins(con):
    """
    Initializes the database for the "02_inner_joins" theme by creating tables and
    populating them with data. It also sets up several exercises and their questions
    related to inner joins.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
    """

    # Table des commandes:
    orders_data = {
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [101, 102, 103, 104, 105],
    }
    df_orders = pd.DataFrame(orders_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_orders AS SELECT * FROM df_orders")

    # Table des clients
    customers_data = {
        "customer_id": [101, 102, 103, 104, 105, 106],
        "customer_name": [
            "Toufik",
            "Daniel",
            "Tancrède",
            "Kaouter",
            "Jean-Nicolas",
            "David",
        ],
    }
    df_customers = pd.DataFrame(customers_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM df_customers")

    # Table des produits
    p_names = ["Laptop", "Ipad", "Livre", "Petitos"]
    products_data = {
        "product_id": [101, 103, 104, 105],
        "product_name": p_names,
        "product_price": [800, 400, 30, 2],
    }

    df_products = pd.DataFrame(products_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_products AS SELECT * FROM df_products")

    # Détail des commandes
    order_details_data = {
        "order_id": [1, 2, 3, 4, 5],
        "product_id": [102, 104, 101, 103, 105],
        "quantity": [2, 1, 3, 2, 1],
    }

    df_order_details = pd.DataFrame(order_details_data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS df_order_details AS SELECT * FROM df_order_details"
    )

    # Ex01 - Commandes détaillées
    detailed_order = pd.merge(df_orders, df_order_details, on="order_id", how="inner")
    con.execute(
        "CREATE TABLE IF NOT EXISTS detailed_order AS SELECT * FROM detailed_order"
    )

    # Ex02 - Commandes des clients détaillées
    order_client = pd.merge(df_customers, detailed_order, on="customer_id", how="inner")
    con.execute("CREATE TABLE IF NOT EXISTS order_client AS SELECT * FROM order_client")

    # Définir les exercices, questions et tables associées
    exercises = [
        {
            "exercise_name": "ex01_orders_and_order_details",
            "tables": ["df_orders", "df_order_details"],
            "question": "Effectuez un INNER JOIN entre les commandes et leurs détails.",
        },
        {
            "exercise_name": "ex02_orders_and_clients",
            "tables": ["df_customers", "detailed_order"],
            "question": "Réalisez un INNER JOIN entre les clients et les commandes détaillées.",
        },
        {
            "exercise_name": "ex03_order_clients_and_products",
            "tables": ["order_client", "df_products"],
            "question": "Effectuez un INNER JOIN entre les clients des commandes détaillées et les produits.",
        },
    ]

    # Insérer les exercices dans `memory_state` et les questions dans `exercise_questions`
    for exercise in exercises:
        exercise_name = exercise["exercise_name"]
        tables = json.dumps(exercise["tables"])  # Convertir en JSON
        question = exercise["question"]

        # Vérifier si l'exercice existe déjà dans memory_state
        existing_exercise = con.execute(
            """
            SELECT last_reviewed FROM memory_state 
            WHERE theme = '02_inner_joins' AND exercise_name = ?
            """,
            (exercise_name,),
        ).fetchone()

        if not existing_exercise:
            # Ajouter dans `memory_state`
            con.execute(
                f"""
                INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
                VALUES (
                    '02_inner_joins',
                    '{exercise_name}',
                    '{tables}', 
                    '{date.today()}'
                 )
                """
            )

        # Ajouter dans `exercise_questions`
        con.execute(
            """
            INSERT OR IGNORE INTO exercise_questions (theme, exercise_name, question)
            VALUES (?, ?, ?)
            """,
            ("02_inner_joins", exercise_name, question),
        )
