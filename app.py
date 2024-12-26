# pylint: disable=missing-module-docstring

import ast
import logging
import os
from datetime import date, timedelta
from typing import Optional, Tuple

import duckdb
import pandas as pd
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
# subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by
    1 : checking the columns
    2 : checking the values
    :param user_query: a string containing the query inserted by the user
    :return:
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


def get_exercise(
    con,
) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[pd.DataFrame]]:
    """
    Select a theme and return the corresponding exercise, its SQL solution, and its dataframe.

    :param con: Connection to the DuckDB database.
    :return: A tuple containing:
             - exercise (pd.DataFrame): The exercise DataFrame.
             - answer (str): The SQL solution as a string.
             - solution_df (pd.DataFrame): The solution DataFrame.
             If an error occurs, returns (None, None, None).
    """

    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write("You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = "SELECT * FROM memory_state"
    exercise_df = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise_df)
    exercise_name = exercise_df.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        sql_answer = f.read()
    solution = con.execute(sql_answer).df()

    return exercise_df, sql_answer, solution


with st.sidebar:
    exercise, answer, solution_df = get_exercise(con)

st.header("Enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")


if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"""
            UPDATE memory_state SET last_reviewed = '{next_review}' 
            WHERE exercise_name = '{exercise.loc[0, 'exercise_name']}'
            """
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.code(answer)
