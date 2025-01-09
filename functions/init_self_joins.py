import random
from datetime import date

random.seed(42)
import pandas as pd


def init_self_joins(con):
    """
    Initializes the database schema and populates the tables required for exercises
    involving self-joins. This function creates a table simulating sales data and
    prepares an exercise where self-joins are used to identify specific patterns.

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
        f"""
        INSERT OR IGNORE INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '05_self_joins',
             'ex01_df_sales',
             '["df_sales"]',
             '{date.today()}'
             )
        """
    )

    # Insérer la question pour l'exercice dans `exercise_questions`
    con.execute(
        """
        INSERT INTO exercise_questions (theme, exercise_name, question)
        VALUES (
            '05_self_joins',
            'ex01_df_sales',
            'Identifiez les clients ayant effectué des achats sur deux jours consécutifs en utilisant un self-join.'
        )
        ON CONFLICT (theme, exercise_name) DO NOTHING;
        """
    )
