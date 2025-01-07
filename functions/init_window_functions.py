import json

import pandas as pd


def init_window_functions(con):
    """

    :param con:
    :return:
    """

    # Capteurs Table
    df_capteurs = pd.read_csv("data/09_window_functions/capteur_a_retrail.csv")
    con.execute("CREATE TABLE IF NOT EXISTS df_capteurs AS SELECT * FROM df_capteurs")

    # Wages table
    data = {
        "name": [
            "Toufik",
            "Jean-Nicolas",
            "Daniel",
            "Kaouter",
            "Sylvie",
            "Sebastien",
            "Diane",
            "Romain",
            "François",
            "Anna",
            "Zeinaba",
            "Gregory",
            "Karima",
            "Arthur",
            "Benjamin",
        ],
        "wage": [
            60000,
            75000,
            55000,
            80000,
            70000,
            90000,
            65000,
            72000,
            68000,
            85000,
            100000,
            120000,
            95000,
            83000,
            110000,
        ],
        "department": [
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "CEO",
        ],
    }
    wages = pd.DataFrame(data)
    wages.assign(
        max_per_dpt=lambda df_: df_[["department", "wage"]]
        .groupby("department")
        .transform("max")
    ).sort_values("department")
    con.execute("CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages")

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
                        "sur les records restants" ,
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
