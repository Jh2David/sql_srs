import json
import random
from datetime import date

import pandas as pd


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
    # APARTMENTS
    appt_nord = pd.read_csv("data/06_group_by/appartements_nord_pdc.csv")
    con.execute("CREATE TABLE IF NOT EXISTS appt_nord AS SELECT * FROM appt_nord")

    # FIND THE BEST CLIENTS
    # Other dataframe for exercices 7A to 7D. Clients table
    clients = [
        "Oussama",
        "Julie",
        "Chris",
        "Tom",
        "Jean-Nicolas",
        "Aline",
        "Ben",
        "Toufik",
        "Sylvie",
        "David",
    ]
    df_ventes = [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2

    df_ventes = pd.DataFrame(df_ventes)
    df_ventes.columns = ["montant"]
    df_ventes["client"] = clients * 3
    con.execute("CREATE TABLE IF NOT EXISTS df_ventes AS SELECT * FROM df_ventes")

    # Other dataframe for exercices 8A to 8B. Clients table
    person_names = ["Benjamin", "Florian", "Tarik", "Bob", "Sirine", "Alice"]

    # MEETINGS
    # Data for the meetings
    meetings_data = []
    for meeting_id in range(150):
        persons_in_meet = random.sample(person_names, random.randint(1, 5))
        for person_name in persons_in_meet:
            meetings_data.append((meeting_id, person_name))

    meetings_df = pd.DataFrame(meetings_data, columns=["meeting_id", "person_name"])

    # Duration meeting
    meeting_durations = []
    for meeting_id in meetings_df["meeting_id"].unique():
        duration = random.randint(10, 45)  # You can adjust the range as needed
        meeting_durations.append((meeting_id, duration))

    durations_df = pd.DataFrame(
        meeting_durations, columns=["meeting_id", "duration_minutes"]
    )

    # Data Tweak
    average_duration = durations_df["duration_minutes"].mean()
    meetings_with_flo = meetings_df[meetings_df["person_name"] == "Florian"][
        "meeting_id"
    ].unique()
    for _, row in durations_df.iterrows():
        if row["meeting_id"] in meetings_with_flo:
            row["duration_minutes"] += random.randint(
                50, 65
            )  # Add extra minutes to meet the condition

    # Total
    merged_df = meetings_df.merge(durations_df, on="meeting_id")
    con.execute("CREATE TABLE IF NOT EXISTS merged_df AS SELECT * FROM merged_df")

    # Table des questions
    exercises_and_questions = [
        {
            "exercise_name": "ex01_group_by_appt_nord",
            "tables": ["appt_nord"],
            "question": "Combien de ventes ont été réalisées par commune ?",
        },
        {
            "exercise_name": "ex02_group_by_appt_nord",
            "tables": ["appt_nord"],
            "question": "Quelle est la moyenne des prix par commune ?",
        },
        {
            "exercise_name": "ex03_group_by_appt_nord",
            "tables": ["appt_nord"],
            "question": "Quelle est la moyenne des prix par commune et le nombre de logements associé (nb_lines) ?",
        },
        {
            "exercise_name": "ex04_where_and_subquery_appt_nord",
            "tables": ["appt_nord"],
            "question": "Appliquez une clause WHERE et une subquery pour sélectionner les communes proposant plus de 10 logements (nb_lines>10) .",
        },
        {
            "exercise_name": "ex05_where_and_CTE_appt_nord",
            "tables": ["appt_nord"],
            "question": "Utilisez une CTE pour sélectionner les communes proposant plus de 10 logements (nb_lines>10)",
        },
        {
            "exercise_name": "ex06_where_and_having_appt_nord",
            "tables": ["appt_nord"],
            "question": "Utiliser une clause HAVING pour filtrer les communes proposant plus de 10 logements (nb_lines>10)",
        },
        {
            "exercise_name": "ex07A_find_the_best_customers_df_ventes",
            "tables": ["df_ventes"],
            "question": "Calculer le panier moyen pour chaque client",
        },
        {
            "exercise_name": "ex07B_find_the_best_customers_df_ventes",
            "tables": ["df_ventes"],
            "question": "Votre PO vous demande de sortir la liste des clients qui ont des achats supérieurs à la moyenne (avec subquery) ",
        },
        {
            "exercise_name": "ex07C_find_the_best_customers_df_ventes",
            "tables": ["df_ventes"],
            "question": "Votre PO vous demande de sortir la liste des clients qui ont des achats supérieurs à la moyenne (avec CTE) ",
        },
        {
            "exercise_name": "ex07D_find_the_best_customers_df_ventes",
            "tables": ["df_ventes"],
            "question": "Quelle est la moyenne de la somme des ventes ? \n"
            "Utilisez une CTE pour obtenir les clients qui ont un total d'achat supérieur à la moyenne des totaux d'achats "
            "des autres clients \n"
            "Etapes: \n"
            "- Faire une query pour obtenir les ventes totales par client \n"
            "- La stocker dans une subquery \n"
            "- A partir de cette subquery, faire un query pour obtenir la moyenne de ces ventes totales \n"
            "- La stocker dans une 2nde subquery \n"
            "- A partir de cette deuxième subquery, récupérer les clients et leur somme totales dépensées, et filtrer "
            "sur les clients dont la moyenne est supérieure à celle calculée dans la 2e subquery",
        },
        {
            "exercise_name": "ex08A_meetings_merged_df",
            "tables": ["merged_df"],
            "question": "Faites le SELF JOIN \n"
            "- Créer une table avec toutes les combinaisons de personnes ayant assisté au même meeting \n"
            "- Ne garder que les records qui me concernent (Benjamin) \n"
            "- Enlever les records où je suis en réunion 'avec moi-même'",
        },
        {
            "exercise_name": "ex08B_meetings_merged_df",
            "tables": ["merged_df"],
            "question": "Quels sont les collègues vous incitant à faire de longues réunions ?\n"
            "- Calculez la durée moyenne des meetings avec chaque collègue \n"
            "- Faire un group by pour savoir la durée moyenne de mes meetings avec chaque personne \n"
            "- Ne garder que les résultats pour lesquels la moyenne est > à 1h",
        },
    ]

    # Insérer les exercices et les questions
    for exercise in exercises_and_questions:
        exercise_name = exercise["exercise_name"]
        tables = json.dumps(exercise["tables"])
        question = exercise["question"]

        # QUESTIONS
        con.execute(
            """
                    INSERT INTO exercise_questions (theme, exercise_name, question)
                    VALUES (?, ?, ?)
                """,
            ("06_group_by", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
            INSERT OR IGNORE INTO memory_state (theme, exercise_name, tables, last_reviewed)
            VALUES (
                '06_group_by',
                 '{exercise_name}',
                 '{tables}',
                 '{date.today()}'
                 )
            """
        )
