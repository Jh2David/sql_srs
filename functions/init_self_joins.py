import random

random.seed(42)
import pandas as pd


def init_self_joins(con):
    """
    Initializes the database schema and populates the tables required for exercises
    involving self-joins. This function creates a table simulating sales data and
    prepares an exercise where self-joins are used to identify specific patterns.

    Tables created:
        - df_sales: Contains sales data with columns for order ID, customer ID,
          and the day on which the order was placed.

    Exercise added to `memory_state`:
        - `ex01_df_sales`: The goal is to identify customers who made purchases on
          two consecutive days using a self-join. The steps for this exercise include:
          1. Performing a self-join on `df_sales` to find all combinations of orders
             for the same customer.
          2. Excluding rows where the same order appears twice.
          3. Filtering rows where the difference between the two dates is exactly 1.

    Args:
        con: A DuckDB connection object used to execute SQL commands.

    Returns:
        None
    """

    # Table des employés
    sales = {
        "order_id": list(range(1110, 1198)),
        "customer_id": random.choices([11, 12, 13, 14, 15, 11, 12, 13, 14], k=88),
    }
    df_sales = pd.DataFrame(sales)
    df_sales["date"] = [d // 3 + 1 for d in range(1, 89)]
    con.execute("CREATE TABLE IF NOT EXISTS df_sales AS SELECT * FROM df_sales")

    # ----------------------------------------------------------------------------------
    # EXERCICE 01
    # ----------------------------------------------------------------------------------
    # Retrouver tous les clients qui sont venus deux jours de suite
    # - Faire un self join pour avoir toutes les combinaisons de commandes possibles pour un même client
    # - Retirer les lignes qui correspondent à la combinaison de la même commande
    # - Récupérer les lignes où la difference entre la première date et la seconde est = 1

    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '05_self_joins',
             'ex01_df_sales',
             '["df_sales"]',
             '1970-01-01'
             )
        """
    )
