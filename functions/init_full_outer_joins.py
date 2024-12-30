import pandas as pd


def init_full_outer_joins(con):
    """
    Initializes the database schema and populates the tables required for exercises
    involving full outer joins. This function creates tables for customers, stores, products,
    and relationships between them, then prepares an exercise based on these tables.

    Tables created:
        - df_customers: Contains customers with their IDs and names.
        - df_store_products: Maps stores to the products they sell.
        - products_data: Stores product details (ID, name, price).
        - df_stores: Lists stores and their associated customer IDs.
        - detailed_order: Combines customers with their associated stores (via a left join).
        - stores_and_products: Extends detailed orders with products sold by the stores (via a left join).

    Exercise added to `memory_state`:
        - `ex01_stores_and_products_and_df_products`: Uses a full outer join to combine
          `stores_and_products` with product details.

    Args:
        con: A DuckDB connection object used to execute SQL commands.

    Return:
        None
    """
    # Table des clients
    customers_data = {
        "customer_id": [11, 12, 13, 14, 15],
        "customer_name": ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"],
    }
    df_customers = pd.DataFrame(customers_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM df_customers")

    # produits vendus
    store_products_data = {
        "store_id": [1, 1, 1, 2, 2, 3, 4],
        "product_id": [101, 103, 105, 101, 103, 104, 105],
    }
    df_store_products = pd.DataFrame(store_products_data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS df_store_products AS SELECT * FROM df_store_products"
    )

    # Table des produits
    p_names = [
        "Cherry coke",
        "Laptop",
        "Ipad",
        "Livre",
    ]
    products_data = {
        "product_id": [100, 101, 103, 104],
        "product_name": p_names,
        "product_price": [3, 800, 400, 30],
    }
    df_products = pd.DataFrame(products_data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS products_data AS SELECT * FROM products_data"
    )

    # Table des stores:
    stores_data = {"store_id": [1, 2, 3, 4], "customer_id": [11, 12, 13, 15]}
    df_stores = pd.DataFrame(stores_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_stores AS SELECT * FROM df_stores")

    # Exercice 1 : left join pour rassembler les clients avec leurs stores
    detailed_order = pd.merge(df_customers, df_stores, on="customer_id", how="left")
    con.execute(
        "CREATE TABLE IF NOT EXISTS detailed_order AS SELECT * FROM detailed_order"
    )

    # Exercice 2 : left join pour rassembler les clients et leurs stores avec les produits qu'ils vendent
    stores_and_products = pd.merge(
        detailed_order, df_store_products, on="store_id", how="left"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS stores_and_products AS SELECT * FROM stores_and_products"
    )

    # ----------------------------------------------------------------------------------
    # EXERCICE 01
    # ----------------------------------------------------------------------------------
    # Exercice 3 (voir cours) : outer join pour rassembler les stores_et_produits avec le détail des produits
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '04_full_outer_joins',
             'ex01_stores_and_products_and_df_products',
             '["stores_and_products", "df_products"]',
             '1970-01-01'
             )
        """
    )
