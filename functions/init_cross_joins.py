import pandas as pd
import io
import duckdb

def init_cross_joins(con):
    # Exemple de données pour cross join
    csv = """
    beverage,price
    orange juice,2.5
    Expresso,2
    Tea,3
    """
    beverages = pd.read_csv(io.StringIO(csv))
    con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

    csv2 = """
    food_item,food_price
    cookie juice,2.5
    chocolatine,2
    muffin,3
    """
    food_items = pd.read_csv(io.StringIO(csv2))
    con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

    # Ajoute des exercices à la table `memory_state` pour ce type de jointure
    data = {
        "theme": ["cross_joins"],
        "exercise_name": ["beverages_and_food"],
        "tables": [["beverages", "food_items"]],
        "last_reviewed": ["1980-01-01"],
    }
    memory_state_df = pd.DataFrame(data)
    con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")