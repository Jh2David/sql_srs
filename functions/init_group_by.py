import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load data from the CSV file and return it as a DataFrame.

    :return: pd.DataFrame containing the data from the CSV file.
    """
    return pd.read_csv("data/06_group_by/appartements_nord_pdc.csv")

def init_group_by(con):
    """
    Initializes the database for the "06_group_by" theme by creating a table and populating
    it with data from a CSV file. It also sets up several exercises related to the theme.

    Steps performed:
    1. Loads the `appartements_nord_pdc.csv` file into a Pandas DataFrame.
    2. Creates the `appt_nord` table in the database if it doesn't already exist and populates it with the DataFrame data.
    3. Inserts exercise definitions into the `memory_state` table for various GROUP BY-related exercises.

    :param con: DuckDB connection object to execute SQL queries.
    :return: None
    """
    appt_nord = load_data()
    con.execute("CREATE TABLE IF NOT EXISTS appt_nord AS SELECT * FROM appt_nord")

    # Nombre de ventes par commune
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex01_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # La moyenne des prix par commune
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex02_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Moyenne et count du nombre de lignes
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex03_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et subquery
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex04_where_and_subquery_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et CTE
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex05_where_and_CTE_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et having
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex06_where_and_having_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )
