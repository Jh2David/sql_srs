import streamlit as st
import pandas as pd
import duckdb

st.write("Hello world")
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)
st.dataframe(df)

sql_query = st.text_area(label="Entrer votre input")
result = duckdb.sql(sql_query).df()
st.code(f"Vous avez entré la query suivante : \n{sql_query}")

st.dataframe(result)