import json

import pandas as pd


def init_left_joins(con):
    """
    Initializes the database schema and populates the tables required for exercises
    involving left joins. The function creates several tables and inserts corresponding
    exercises into the `memory_state` table.

    Tables created:
        - df_orders: Contains orders with their IDs and associated customer IDs.
        - df_customers: Lists customers with their IDs and names.
        - df_products: Stores product details (ID, name, price).
        - df_order_details: Links orders to products with their quantities.
        - detailed_order: Combines orders with their corresponding details (via a left join).
        - order_client: Extends detailed_order with customer information (via a left join).

    Exercises added to `memory_state`:
        1. `ex01_orders_and_order_details`: Combines `df_orders` and `df_order_details`.
        2. `ex02_orders_and_clients`: Extends detailed orders with customer details.
        3. `ex03_order_clients_and_products`: Combines customer-detailed orders with products.

    Args:
        con: A DuckDB connection object used to execute SQL commands.

    Returns:
        None
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
    detailed_order = pd.merge(df_orders, df_order_details, on="order_id", how="left")
    con.execute(
        "CREATE TABLE IF NOT EXISTS detailed_order AS SELECT * FROM detailed_order"
    )

    # Ex02 - Commandes des clients détaillées
    order_client = pd.merge(df_customers, detailed_order, on="customer_id", how="left")
    con.execute("CREATE TABLE IF NOT EXISTS order_client AS SELECT * FROM order_client")


    # ----------------------------------------------------------------------------------
    # Table des questions pour chaque exercice
    # ----------------------------------------------------------------------------------
    exercises = [
        {
            "exercise_name": "ex01_orders_and_order_details",
            "tables": ["df_orders", "df_order_details"],
            "question": "Effectuez un LEFT JOIN entre les commandes et leurs détails.",
        },
        {
            "exercise_name": "ex02_orders_and_clients",
            "tables": ["df_customers", "detailed_order"],
            "question": "Réalisez un LEFT JOIN entre les clients et les commandes détaillées.",
        },
        {
            "exercise_name": "ex03_order_clients_and_products",
            "tables": ["order_client", "df_products"],
            "question": "Effectuez un LEFT JOIN entre les clients des commandes détaillées et les produits.",
        },
    ]

    # Insérer les exercices dans `memory_state` et les questions dans `exercise_questions`
    for exercise in exercises:
        exercise_name = exercise["exercise_name"]
        tables = json.dumps(exercise["tables"])  # Convertir en JSON
        question = exercise["question"]

        # Ajouter dans `memory_state`
        con.execute(
            f"""
              INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
              VALUES (
                  '03_left_joins',
                  '{exercise_name}',
                  '{tables}',
                  '1970-01-01'
                  )
              """
        )

        # Ajouter dans `exercise_questions`
        con.execute(
            """
            INSERT INTO exercise_questions (theme, exercise_name, question)
            VALUES (?, ?, ?)
            """,
            ("03_left_joins", exercise_name, question),
        )
