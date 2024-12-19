import streamlit as st
import pandas as pd
import duckdb
import io

st.write("""
# SQL SRS
Space Repetition System SQL practice
""")

option = st.selectbox(
    "How would you like to review?",
    ("Joins", "GroupBy", "Windows Functions"),
    index=None,
    placeholder="Select a theme...",
)

st.write("You selected:", option)



csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer).df()

st.header("Enter your code")

sql_query = st.text_area(label="votre code SQL ici", key="user_input")
if sql_query:
    result = duckdb.sql(sql_query).df()
    st.code(f"Vous avez entré la query suivante : \n{result}")


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table : beverages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("expected :")
    st.dataframe(solution)

with tab3:
    st.code(answer)