# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "How would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("You selected:", option)

st.header("Enter your code")
sql_query = st.text_area(label="votre code SQL ici", key="user_input")
if sql_query:
    result = duckdb.sql(sql_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if n_lines_differences != 0:
        st.write(
            f"result has a {n_lines_differences} lines difference with the solution_df"
        )

    st.dataframe(result.compare(solution_df))

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table : beverages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("expected :")
    st.dataframe(solution_df)

with tab3:
    st.code(ANSWER_STR)
