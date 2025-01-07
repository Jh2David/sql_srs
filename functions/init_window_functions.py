import json

import pandas as pd
import random

def init_window_functions(con):
    """

    :param con:
    :return:
    """

    # Capteur A Table
    df_capteurs = pd.read_csv("data/09_window_functions/capteur_a_retrail.csv")
    con.execute("CREATE TABLE IF NOT EXISTS df_capteurs AS SELECT * FROM df_capteurs")

    # Capteurs A & B Table
    random.seed(42)
    df_porte_b = df_capteurs.copy()
    # On ajoute une porte_b
    df_porte_b["capteur_id"] = "porte_b"
    df_porte_b["visiteurs_count"] = df_porte_b["visiteurs_count"].apply(lambda x: round(x * (random.random() + 0.5), 0))
    df_capteurs_A_B = pd.concat([df_capteurs, df_porte_b])
    con.execute("CREATE TABLE IF NOT EXISTS df_capteurs_A_B AS SELECT * FROM df_capteurs_A_B")

    # Wages table
    data = {
    'name': ['Toufik', 'Jean-Nicolas', 'Daniel', 'Kaouter', 'Sylvie',
             'Sebastien', 'Diane', 'Romain', 'François', 'Anna',
             'Zeinaba', 'Gregory', 'Karima', 'Arthur', 'Benjamin'],
    'wage': [60000, 75000, 55000, 100000, 70000,
             90000, 65000, 100000, 68000, 85000,
             100000, 120000, 95000, 83000, 110000],
    'department': ['IT', 'HR', 'SALES', 'IT', 'IT',
                   'HR', 'SALES', 'IT', 'HR', 'SALES',
                   'IT', 'IT', 'HR', 'SALES', 'CEO'],
    'sex': ['H', 'H', 'H', 'F', 'F',
           'H', 'F', 'H', 'H', 'F',
           'F', 'H', 'F', 'H', 'H',]
}
    wages = pd.DataFrame(data)
    con.execute("DROP TABLE wages;"
                "CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages")

    exercises_and_questions = [
        {
            "exercise_name": "ex01A_over_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Utilisez OVER() pour avoir le total des visiteurs sur l'ensemble de la table, "
            "dans une nouvelle colonne 'total_visiteurs'",
        },
        {
            "exercise_name": "ex01B_over_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Votre manager veut que la colonne total contienne le total progressif des visiteurs sur le mois.",
        },
        {
            "exercise_name": "ex01C_over_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Il veut maintenant avoir une moyenne de visiteurs sur le mois qui se met à jour progressivement"
            " en fonction des résultats de la journée",
        },
        {
            "exercise_name": "ex01D_rows_between_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Le P.O. estime qu'il n'est pas nécessaire de garder les anciennes valeurs au delà d'une semaine. "
            "Il veut un 'moving average' uniquement sur les 7 derniers jours.",
        },
        {
            "exercise_name": "ex01E_rows_between_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Vérification de cette moyenne mobile\n"
            "- Ajouter le running total sur les sept derniers jours\n"
            "- Le count(*) sur les sept derniers jours\n "
            "- La division de ce running_total par le count pour comparer avec la moyenne précédemment obtenue",
        },
        {
            "exercise_name": "ex02A_partition_by_wages",
            "tables": ["wages"],
            "question": "Quel est le plus gros salaire par département?",
        },
        {
            "exercise_name": "ex02B_partition_by_wages",
            "tables": ["wages"],
            "question": "Maintenant, on aimerait le plus gros salaire par département en face de chaque salaire pour "
            "calculer les écarts de salaires entre les employés d'un même département\n"
            "Il faut imaginer que vous faites une 'sous-table' pour chaque département (max_dpt_wage), "
            "et un MAX(wage) OVER() pour chacune de ces sous-tables",
        },
        {
            "exercise_name": "ex02C_partition_by_wages",
            "tables": ["wages"],
            "question": "Calculer le salaire moyen par département (mean_dpt_wage)",
        },
        {
            "exercise_name": "ex02D_partition_by_wages",
            "tables": ["wages"],
            "question": "Créez une nouvelle colonne 'is_max' qui indique si un salarié est au max de son département "
            "(max_dpt_wage)",
        },
        {
            "exercise_name": "ex02E_partition_by_wages",
            "tables": ["wages"],
            "question": "Utiliser la colonne 'is_max' pour déterminer les salariés ayant le 2ème salaire max\n"
            "Hint : Utilisez une CTE pour stocker le 1er salaire maximum par département, puis filtrer "
            "cette CTE pour exclure le MAX et refaites la même procédure pour trouver le nouveau MAX "
            "sur les records restants",
        },
        {
            "exercise_name": "ex01F_partition_by_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Mettez en face de chaque visiteurs_count la moyenne sur les 7 derniers jours, en partitionnant "
            "la table en fonction du jour de la semaine, puis multipliez cette colonne par 0.8 pour créer "
            "votre nouveau seuil\n"
            "Note : Contrairement à l'ex01E, il s'agit de la moyenne glissante (ou mobile), cela permet par "
            "exemple de faire la moyenne des 7 derniers samedi au lieu des 7 derniers jours de la semaine",
        },
        {
            "exercise_name": "ex01G_partition_by_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Attention ! \n"
            "Il se trouve que la dataframe de l'ex01F était ordonée par date, mais rien ne garantit que ce "
            "sera toujours le cas! \n"
            "Que se passerait-il si les jours n'étaient pas correctement ordonnés?\n"
            "Hint : Pour être sur que les données sont correctement triées avant de calculer les "
            "indicateurs, il faut utiliser ORDER BY à l'intérieur de la clause OVER.",
        },
        {
            "exercise_name": "ex01H_lag_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Utilisez LAG() afin de déterminer le nombre de visiteurs de la ligne précédente "
            "(AS ligne_precedente) ",
        },
        {
            "exercise_name": "ex01I_lag_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "LAG after WHERE\n"
            "On pourrait s'attendre à ce que le LAG soit opéré sur l'ensemble de la table, et que le WHERE "
            "vienne ensuite filtrer et rendre l'interprétation difficile. Mais ce n'est pas ce qui se passe. "
            "Utilisez par exemple WHERE weekday = 7 pour confirmer cela",
        },
        {
            "exercise_name": "ex01J_lag_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "LAG sur toute la dataframe\n"
            "Exercice: mettez, en face de chaque 'visiteurs_count', le visiteurs_count du même jour de la "
            "semaine précédente",
        },
        {
            "exercise_name": "ex01K_lag_df_capteurs",
            "tables": ["df_capteurs"],
            "question": "Déterminer la différence visiteurs_count et lag_visiteurs_count calculé dans l'exercice précédent "
            "(ex01J)\n"
            "Si vous êtes motivés, calculez le pourcentage de changement d'une semaine sur l'autre "
            "(AS pct_change, toujours pour le même jour)",
        },
        {
            "exercise_name": "ex02F_row_number_wages",
            "tables": ["wages"],
            "question": "Déterminer l'index de la table\n"
                        "Il s'agit tout simplement de connaître le numéro de la ligne",
        },
        {
            "exercise_name": "ex02G_row_number_wages",
            "tables": ["wages"],
            "question": "Déterminer maintenant le numéro de ligne par département l'index de la table",
        },
        {
            "exercise_name": "ex02H_row_number_wages",
            "tables": ["wages"],
            "question": "Obtenez le classement entre les hommes et les femmes",
        },
        {
            "exercise_name": "ex02I_row_number_wages",
            "tables": ["wages"],
            "question": "Déterminez le numéro de ligne par département, du plus gros au plus petit salaire (LIMIT 10)",
        },
        {
            "exercise_name": "ex02J_row_number_wages",
            "tables": ["wages"],
            "question": "Obtenez le classement des salaires par sexe (LIMIT 10)",
        },
        {
            "exercise_name": "ex02K_rank_wages",
            "tables": ["wages"],
            "question": "Comment gérer les égalités?\n"
                        "Obtenez le classement des salaires, du plus gros au plus petit, et par département.\n"
                        "Utilisez RANK() (LIMIT 10)",
        },
        {
            "exercise_name": "ex02L_rank_wages",
            "tables": ["wages"],
            "question": "Comment gérer les égalités?\n"
                        "Obtenez le classement des salaires, du plus gros au plus petit, et par département.\n"
                        "Utilisez DENSE_RANK() (LIMIT 10)",
        },
        {
            "exercise_name": "ex02M_rank_wages",
            "tables": ["wages"],
            "question": "Obtenez le classement des salaires par sexe.\n"
                        "(S'il y a une égalité pour la première place, on souhaite que le 3ème ait le rang '2')",
        },
        {
            "exercise_name": "ex03A_df_capteurs_A_B",
            "tables": ["df_capteurs_A_B"],
            "question": "Faites une requête pour avoir la moyenne glissante des visiteurs les Samedi, pour le capteur "
                        "porte_a et le capteur porte_b\n"
                        "Utilisez la clause WHERE weekday = 7\n"
                        "Mais attention, cette requête fonctionne parce que le fenêtrage se fait sur la donnée restante "
                        "après la clause WHERE\n"
                        "Si on enlève le WHERE weekday = 7, les calculs ne sont plus bons",
        },
        {
            "exercise_name": "ex03B_df_capteurs_A_B",
            "tables": ["df_capteurs_A_B"],
            "question": "Faites une requête pour avoir la moyenne glissante des visiteurs sur l'ensemble de la donnée, "
                        "pour le capteur porte_a et le capteur porte_b\n"
                        "On souhaite tous les jours de la semaine, c'est-à-dire la moyenne pour tous les lundi, "
                        "les mardi, etc.\n"
                        "On n'utilise plus cette fois-ci la clause WHERE\n"
        },
        {
            "exercise_name": "ex03C_df_capteurs_A_B",
            "tables": ["df_capteurs_A_B"],
            "question": "Déterminer le classement entre les capteurs A et B (AS updated_ranking), quel est celui chaque "
                        "semaine qui a le plus de visiteurs?\n"
                        "Hint : Utiliser une CTE de la moyenne glissante des visiteurs sur l\'ensemble de "
                        "la donnée (ex03B)"
        },
        {
            "exercise_name": "ex02N_qualify_wages",
            "tables": ["wages"],
            "question": "Déterminer les salariés ayant le 2ème salaire max par département en opérant un filtrage index = 2\n"
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
            ("09_window_functions", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
                      INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
                      VALUES (
                          '09_window_functions',
                           '{exercise_name}',
                           '{tables}',
                           '1970-01-01'
                           )
                      """
        )
