# pylint: disable=missing-module-docstring

import ast
import os
from datetime import date, timedelta
from typing import Optional, Tuple

import duckdb
import pandas as pd
import streamlit as st
from streamlit_ace import st_ace

# Initialisation des dossiers
if "data" not in os.listdir():
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Initialisation des états Streamlit
if "validated_count" not in st.session_state:
    st.session_state.validated_count = 0  # Compteur d'exercices validés

if "validated_exercises" not in st.session_state:
    st.session_state.validated_exercises = set()  # Ensemble des exercices validés

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""


def check_users_solution(user_query: str) -> None:
    """
    Check the user's SQL query against the solution and display results.
    """
    global solution_df
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.success("Résultat correct !")
            st.balloons()
            current_exercise = st.session_state.exercise_name
            if current_exercise not in st.session_state.validated_exercises:
                st.session_state.validated_exercises.add(current_exercise)
                st.session_state.validated_count += 1
                st.info(f"Exercice validé!")
            else:
                st.info(f"L'exercice '{current_exercise}' est déjà validé.")
        else:
            st.warning("Le résultat n'est pas correct.")
    except KeyError:
        st.error("Certaines colonnes manquent.")


def get_exercise(con) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[pd.DataFrame], Optional[str]]:
    """
    Retrieve the exercise, its SQL solution, and its associated question.

    :param con: Connection to the DuckDB database.
    :return: Tuple with exercise_df, sql_answer, solution_df, and sql_question.
    """
    available_themes = ["00_all_themes"] + con.execute(
        "SELECT DISTINCT theme FROM memory_state ORDER BY theme"
    ).df()["theme"].tolist()

    current_theme = st.session_state.get("theme", "00_all_themes")
    if current_theme not in available_themes:
        current_theme = "00_all_themes"

    theme = st.selectbox(
        "What would you like to review?",
        available_themes,
        index=available_themes.index(current_theme),
        placeholder="Select a theme...",
    )

    if theme != st.session_state.get("theme"):
        st.session_state.theme = theme
        st.session_state.user_query = ""
        st.rerun()

    sql_query = (
        "SELECT * FROM memory_state WHERE theme LIKE '0%' ORDER BY last_reviewed"
        if theme == "00_all_themes"
        else f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    )
    exercise_df = con.execute(sql_query).df()

    if exercise_df.empty:
        st.error("No exercises found for this theme.")
        return None, None, None, None

    exercise_df = exercise_df.sort_values("last_reviewed").reset_index(drop=True)

    st.write("### Liste des exercices disponibles")
    st.dataframe(exercise_df)

    exercise_name, actual_theme = exercise_df.loc[0, ["exercise_name", "theme"]]

    if exercise_name != st.session_state.get("exercise_name"):
        st.session_state.exercise_name = exercise_name
        st.session_state.user_query = ""
        st.rerun()

    sql_question_result = con.execute(
        f"""
        SELECT question FROM exercise_questions
        WHERE theme = '{actual_theme}' AND exercise_name = '{exercise_name}'
        """
    ).fetchone()
    sql_question = sql_question_result[0] if sql_question_result else "No question available."

    try:
        with open(f"answers/{actual_theme}/{exercise_name}.sql", "r") as f:
            sql_answer = f.read()
    except FileNotFoundError:
        st.error(f"Solution file for '{exercise_name}' not found in theme '{actual_theme}'.")
        return None, None, None, None

    try:
        solution = con.execute(sql_answer).df()
    except Exception as e:
        st.error(f"Error executing the solution for '{exercise_name}': {e}")
        return None, None, None, None

    return exercise_df, sql_answer, solution, sql_question


# Interface principale
with st.sidebar:
    exercise, answer, solution_df, question = get_exercise(con)

if question:
    st.subheader(question)

query = st_ace(
    value=st.session_state["user_query"],
    placeholder="Écrivez votre code SQL ici",
    language="sql",
    theme="monokai",
    height=300,
    key=f"ace-editor-{st.session_state.exercise_name}",
    font_size=16,
    tab_size=4,
)

if query:
    st.session_state["user_query"] = query
    check_users_solution(query)

# Boutons de révision
col1, col2, col3, col4 = st.columns(4)
days_options = [2, 7, 21]

for i, n_days in enumerate(days_options):
    with [col1, col2, col3][i]:
        if st.button(f"Revoir dans {n_days} jours"):
            next_review = date.today() + timedelta(days=n_days)
            con.execute(
                f"""
                UPDATE memory_state SET last_reviewed = '{next_review}' 
                WHERE exercise_name = '{exercise.loc[0, 'exercise_name']}'
                """
            )
            st.rerun()

# Reset bouton
with col4:
    if st.button("Reset"):
        con.execute(f"UPDATE memory_state SET last_reviewed = '{date.today()}'")
        st.rerun()

# Onglets
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    if exercise is None or exercise.empty:
        st.error("No exercise data found. Please check your theme selection or database.")
    else:
        try:
            exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
            for table in exercise_tables:
                st.write(f"Table: {table}")
                df_table = con.execute(f"SELECT * FROM {table}").df()
                st.dataframe(df_table)
        except (ValueError, SyntaxError) as e:
            st.error(f"Error parsing tables data: {e}")

with tab3:
    st.code(answer)

# Affichage du compteur d'exercices validés
st.sidebar.write(f"**Total des exercices validés**: {st.session_state.validated_count}")