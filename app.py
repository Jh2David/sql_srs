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
) -> Tuple[
    Optional[pd.DataFrame], Optional[str], Optional[pd.DataFrame], Optional[str]
]:
    """
    Select a theme and return the corresponding exercise, its SQL solution, and its dataframe.

    :param con: Connection to the DuckDB database.
    :return: A tuple containing:
             - exercise (pd.DataFrame): The exercise DataFrame.
             - answer (str): The SQL solution as a string.
             - solution_df (pd.DataFrame): The solution DataFrame.
             If an error occurs, returns (None, None, None).
    """

    available_themes_df = con.execute(
        "SELECT DISTINCT theme FROM memory_state ORDER BY theme"
    ).df()

    if "theme" not in st.session_state:
        st.session_state.theme = None

    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=(
            available_themes_df["theme"].unique().tolist().index(st.session_state.theme)
            if st.session_state.theme
            else 0
        ),
        placeholder="Select a theme...",
    )
    # Mettre à jour le thème dans session_state uniquement si sélectionné
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

    # Vérifier si un thème est sélectionné
    if theme is None:
        st.warning("Please select a theme to load the exercises.")
        return None, None, None

    st.write("You selected:", theme)

    select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    exercise_df = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    # Assurez-vous que l'exercice existe
    if exercise_df.empty:
        st.warning("No exercises found for this theme.")
        return None, None, None

    st.dataframe(exercise_df)

    # Choisir le premier exercice
    exercise_name = exercise_df.loc[0, "exercise_name"]

    # Charger la question associée à l'exercice
    sql_question = con.execute(
        f"""
           SELECT question
           FROM exercise_questions
           WHERE theme = '{theme}' AND exercise_name = '{exercise_name}'
       """
    ).fetchone()

    # Vérifier si la question est trouvée
    if sql_question is None:
        st.warning(
            f"No question found for exercise '{exercise_name}' in theme '{theme}'."
        )
        sql_question = "No question available for this exercise."
    else:
        sql_question = sql_question[0]  # Extraire la question du résultat de la requête

    # Charger le fichier SQL de l'exercice
    try:
        with open(f"answers/{theme}/{exercise_name}.sql", "r") as f:
            sql_answer = f.read()
    except FileNotFoundError:
        st.error(f"Solution file for exercise '{exercise_name}' not found.")
        return None, None, None

    solution = con.execute(sql_answer).df()

    return exercise_df, sql_answer, solution, sql_question


# -------------------------------------------------------------------------------
# AFFICHAGE PAGE
# -------------------------------------------------------------------------------
with st.sidebar:
    exercise, answer, solution_df, question = get_exercise(con)

if question:
    st.subheader(question)

query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)

# Ajouter du style CSS pour centrer le texte des boutons et uniformiser leur taille
st.markdown(
    """
<style>
div.stButton {
    width: 100%; /* Pour que le bouton prenne toute la largeur */
    text-align: center; /* Centrer le texte */
    height: 50px; /* Définir une hauteur fixe pour tous les boutons */
}
</style>
""",
    unsafe_allow_html=True,
)


# Fonction pour créer un bouton et gérer la mise à jour
def create_button(col, nb_days):
    with col:
        if st.button(f"Revoir dans {nb_days} jours", use_container_width=True):
            next_review = date.today() + timedelta(days=nb_days)
            con.execute(
                f"""
                UPDATE memory_state SET last_reviewed = '{next_review}' 
                WHERE exercise_name = '{exercise.loc[0, 'exercise_name']}'
                """
            )
            st.rerun()


# Créer 4 colonnes
col1, col2, col3, col4 = st.columns(4)

# Liste des jours pour les boutons
days_options = [2, 7, 21]

# Créer les boutons pour les options de révision
for i, n_days in enumerate(days_options):
    create_button([col1, col2, col3][i], n_days)

# Bouton Reset dans la dernière colonne
with col4:
    if st.button("Reset", use_container_width=True):
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
