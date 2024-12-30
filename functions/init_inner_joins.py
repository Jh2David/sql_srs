import pandas as pd


def init_inner_joins(con):
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

    # ----------------------------------------------------------------------------------
    # EXERCICE 01
    # ----------------------------------------------------------------------------------
    # inner join pour rassembler les commandes avec les détails
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '02_inner_joins',
             'ex01_orders_and_order_details', 
             '["df_orders", "df_order_details"]', 
             '1970-01-01'
             )
    """
    )

    # ----------------------------------------------------------------------------------
    # EXERCISE 02
    # ----------------------------------------------------------------------------------
    # inner join pour rassembler les commandes détaillées avec les clients
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '02_inner_joins',
             'ex02_orders_and_clients', 
             '["df_customers", "detailed_order"]', 
             '1970-01-01'
             )
    """
    )

    # ----------------------------------------------------------------------------------
    # EXERCISE 03
    # ----------------------------------------------------------------------------------
    # inner join pour rassembler les commandes client détaillées avec les produits
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '02_inner_joins',
            'ex03_order_clients_and_products',
            '["order_client", "df_products"]',
            '1970-01-01'
             )
    """
    )
