import json

import pandas as pd

def init_grouping_sets(con):
    """

    :param con:
    :return:
    """

    # Data products store
    data = {
        'store_id': ["Armentieres", "Armentieres", "Armentieres", "Armentieres", "Lille", "Lille", "Lille", "Lille",
                     "Douai", "Douai", "Douai", "Douai"],
        'product_name': ['redbull', 'chips', 'wine', 'redbull', 'redbull', 'chips', 'wine', 'icecream', 'redbull',
                         'chips', 'wine', 'icecream'],
        'amount': [45, 60, 60, 45, 100, 140, 190, 170, 55, 70, 20, 45]
    }
    df_stores_north = pd.DataFrame(data)
    con.execute('CREATE TABLE IF NOT EXISTS df_stores_north AS SELECT * FROM df_stores_north')

    # Population table
    datapop = {
        "year": [2016, 2017, 2018, 2019, 2020] * 3,
        "region": (["IDF"] * 5) + (["HDF"] * 5) + (["PACA"] * 5),
        "population":
            [1010000, 1020000, 1030000, 1040000, 1000000] +
            [910000, 920000, 930000, 940000, 900000] +
            [810000, 820000, 830000, 840000, 950000],
    }
    dfpop = pd.DataFrame(datapop)
    con.execute('CREATE TABLE IF NOT EXISTS dfpop AS SELECT * FROM dfpop')

    # Population real table
    dpt_to_region_mapping = {
        "59": "HDF",
        "62": "HDF",
        "75": "IDF",
        "95": "IDF",
        "83": "PACA",
        "84": "PACA",
    }
    dpts_dfs = []
    for year in range(2016, 2022):
        # https://www.insee.fr/fr/statistiques/1893198
        df = pd.read_excel("data/08_grouping_sets/estim-pop-dep-sexe-gca-1975-2023.xls", str(year), skiprows=3)
        subset = df[df["Départements"].isin(["59", "62", "75", "95", "83", "84"])][["Départements", "Unnamed: 7"]]
        subset["year"] = year
        dpts_dfs.append(subset)

    dpts_dfs = pd.concat(dpts_dfs)
    dpts_dfs.columns = ["departement", "population", "year"]
    dpts_dfs["region"] = dpts_dfs["departement"].apply(lambda x: dpt_to_region_mapping.get(x))

    dpts_dfs = dpts_dfs[["region", "departement", "year", "population"]]
    con.execute('CREATE TABLE IF NOT EXISTS dpts_dfs AS SELECT * FROM dpts_dfs')





    exercises_and_questions = [
        {
            "exercise_name": "ex01A_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Le commercial d'une marque de boisson énergisante veut savoir quel est le magasin de notre "
                        "enseigne qui vend le plus de son produit."
        },
        {
            "exercise_name": "ex01B_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Trouver les magasins qui ont vendu le plus grand nombre de redbull en proportion de leur C.A. "
                        "total \n\n"
                        "Hint :\n"
                        "- Faites une table qui contient une ligne pour chaque magasin et, en face, "
                        "'total_sales' (montant total des ventes de ce magasin)\n" 
                        "- Puis faites une jointure entre la table originale et cette table" 
                        "- Ajoutez à cette jointure la colonne pct_sales, calculée comme suit: "
                        "amount / total_sales\n"
                        "- Problème: on a vendu du redbull deux jours différents à Armentières...\n"
                        "- Utilisez cette nouvelle table pour récupérer le pourcentage des ventes total pour chaque "
                        "produit (SUM + groupby)"
        },
        {
            "exercise_name": "ex01C_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Faites un GROUPING SETS, pour grouper par plusieurs niveaux d'agrégation"
        },
        {
            "exercise_name": "ex01D_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Challenge : \n"
                        "1) Refaites la query avec le GROUPING SETS pour avoir la somme des ventes par:\n" 
                        "(store_id, product_name), et par store_id seul (nommez cette colonne sum_amount)\n"
                        "2) Mettez cette query dans une CTE (appelez la table 'sales_total')\n"
                        "3) Puis joignez cette table avec elle même en utilisant le store_id\n"
                        "4) mettez la colonne 'sum_amount' de la table de gauche dans 'product_sum_amount'\n"
                        "5) mettez la colonne 'sum_amount' de la table de droite dans une autre colonne 'store_sum_amount'\n"
                        "6) Filtrez sur table_de_gauche.product_name = 'redbull' et table_de_droite.product_name IS NULL\n"
        },
        {
            "exercise_name": "ex02_grouping_sets_dfpop",
            "tables": ["dfpop"],
            "question": "Grouper la population par : \n"
                        "- année et région\n"
                        "- année seulement\n"
        },
        {
            "exercise_name": "ex03A_grouping_sets_dpts_dfs",
            "tables": ["dpts_dfs"],
            "question": "Grouping sets sur données de population réelle. \n"
                        "Grouper la population par : \n"
                        "- année et région\n"
                        "- année seulement\n"
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
            ("08_grouping_sets", exercise_name, question),
        )

        # EXERCICES
        con.execute(
            f"""
                  INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
                  VALUES (
                      '08_grouping_sets',
                       '{exercise_name}',
                       '{tables}',
                       '1970-01-01'
                       )
                  """
        )