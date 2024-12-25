import io

import pandas as pd


def init_cross_joins(con):
    # ----------------------------------------------------------------------------------
    # EXERCICE 01
    # ----------------------------------------------------------------------------------
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
    con.execute(
        """
        INSERT INTO memory_state(theme, exercise_name, tables, last_reviewed)
        VALUES ('cross_joins', 'beverages_and_food', '["beverages", "food_items"]', '1970-01-01' )
    """
    )

    # ----------------------------------------------------------------------------------
    # EXERCISE 02
    # ----------------------------------------------------------------------------------
    sizes = """
    size
    XS
    M
    L
    XL
    """
    sizes = pd.read_csv(io.StringIO(sizes))
    con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

    trademarks = """
    trademark
    Nike
    Asphalte
    Abercrombie
    Lewis
    """
    trademarks = pd.read_csv(io.StringIO(trademarks))
    con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

    con.execute(
        """
            INSERT INTO memory_state(theme, exercise_name, tables, last_reviewed)
            VALUES ('cross_joins', 'sizes_and_trademarks', '["sizes", "trademarks"]', '1970-01-01' )
        """
    )

    # ----------------------------------------------------------------------------------
    # EXERCISE 03
    # ----------------------------------------------------------------------------------
    hours = """
    hours
    8
    9
    10
    11
    12
    """
    hours = pd.read_csv(io.StringIO(hours))
    con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours")

    quarters = """
    quarter
    00
    15
    30
    45
    """
    quarters = pd.read_csv(io.StringIO(quarters))
    con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters")

    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES ('cross_joins', 'hours_and_quarters', '["hours", "quarters"]', '1970-01-01')
    """
    )
