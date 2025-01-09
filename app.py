# pylint: disable=missing-module-docstring

import ast
import logging
import os
from datetime import date, timedelta
from typing import Optional, Tuple

import duckdb
import pandas as pd
import streamlit as st
from streamlit_ace import st_ace

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
            st.success("Résultat correct !")
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
             - exercise_df (pd.DataFrame): The exercise DataFrame.
             - sql_answer (str): The SQL solution as a string.
             - solution (pd.DataFrame): The solution DataFrame.
             - sql_question (str): The question for the exercise.
    """

    # Récupération des thèmes disponibles
    available_themes = ["00_all_themes"] + con.execute(
        "SELECT DISTINCT theme FROM memory_state ORDER BY theme"
    ).df()["theme"].tolist()

    # Sélection du thème, avec gestion des erreurs
    current_theme = st.session_state.get("theme", "00_all_themes")
    if current_theme not in available_themes:
        current_theme = "00_all_themes"

    theme = st.selectbox(
        "What would you like to review?",
        available_themes,
        index=available_themes.index(current_theme),
        placeholder="Select a theme...",
    )

    # Mettre à jour le thème dans session_state et redémarrer si nécessaire
    if theme != st.session_state.get("theme"):
        st.session_state.theme = theme
        st.session_state.user_query = ""
        st.rerun()

    # Préparation de la requête SQL en fonction du thème sélectionné
    sql_query = (
        "SELECT * FROM memory_state WHERE theme LIKE '0%' ORDER BY last_reviewed"
        if theme == "00_all_themes"
        else f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    )
    exercise_df = con.execute(sql_query).df()

    # Gestion du cas où aucun exercice n'est trouvé
    if exercise_df.empty:
        st.error("No exercises found for this theme.")
        return None, None, None, None

    # Trier et sélectionner le premier exercice
    exercise_df = exercise_df.sort_values("last_reviewed").reset_index(drop=True)
    st.dataframe(exercise_df)

    exercise_name, actual_theme = exercise_df.loc[0, ["exercise_name", "theme"]]
    if exercise_name != st.session_state.get("exercise_name"):
        st.session_state.exercise_name = exercise_name
        st.session_state.user_query = ""
        st.rerun()

    # Récupération de la question associée
    sql_question_result = con.execute(
        f"""
        SELECT question FROM exercise_questions
        WHERE theme = '{actual_theme}' AND exercise_name = '{exercise_name}'
        """
    ).fetchone()
    sql_question = (
        sql_question_result[0] if sql_question_result else "No question available."
    )

    # Lecture du fichier SQL correspondant
    try:
        with open(f"answers/{actual_theme}/{exercise_name}.sql", "r") as f:
            sql_answer = f.read()
    except FileNotFoundError:
        st.error(
            f"Solution file for '{exercise_name}' not found in theme '{actual_theme}'."
        )
        return None, None, None, None

    # Exécution de la solution SQL
    try:
        solution = con.execute(sql_answer).df()
    except Exception as e:
        st.error(f"Error executing the solution for '{exercise_name}': {e}")
        return None, None, None, None

    return exercise_df, sql_answer, solution, sql_question


# -------------------------------------------------------------------------------
# AFFICHAGE PAGE
# -------------------------------------------------------------------------------
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
    # key="ace-editor",
    font_size=16,
    tab_size=4,
)

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
        con.execute(f"UPDATE memory_state SET last_reviewed = '{date.today()}'")
        st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    # Vérification que 'exercise' n'est ni None ni vide
    if exercise is None or exercise.empty:
        st.error(
            "No exercise data found. Please check your theme selection or database."
        )
    else:
        # Assurer que la colonne 'tables' existe et qu'elle est au bon format
        try:
            exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
            # Afficher les tables si elles existent
            for table in exercise_tables:
                st.write(f"Table: {table}")
                df_table = con.execute(f"SELECT * FROM {table}").df()
                st.dataframe(df_table)
        except (ValueError, SyntaxError) as e:
            st.error(f"Error parsing tables data: {e}")

with tab3:
    st.code(answer)
