import json
from datetime import date

import pandas as pd


def init_grouping_sets(con):
    """
    Initializes the database with sample data and exercises related to SQL Grouping Sets.

    This function creates several tables in the database and populates them with data related to store sales,
    population by region, and insurance reimbursements. It also inserts various exercises and questions concerning
    SQL GROUPING SETS, providing practice scenarios to group and aggregate data in different ways.

    The following tables are created:
    - df_stores_north: Contains sales data for different stores and products.
    - dfpop: Contains population data by year and region.
    - dpts_dfs: Contains population data by department, region, and year.
    - df_assurance_soins: Contains data on insurance reimbursement by contract type and act type.

    Additionally, the function inserts a series of exercises and questions into the `exercise_questions` and
    `memory_state` tables. These exercises cover various use cases for SQL grouping techniques, such as GROUPING SETS,
    ROLLUP, CUBE, FILTER, and CASE WHEN.

    :param con: A connection object to the database.
    :return: None
    """

    # Data products store
    data = {
        "store_id": [
            "Armentieres",
            "Armentieres",
            "Armentieres",
            "Armentieres",
            "Lille",
            "Lille",
            "Lille",
            "Lille",
            "Douai",
            "Douai",
            "Douai",
            "Douai",
        ],
        "product_name": [
            "redbull",
            "chips",
            "wine",
            "redbull",
            "redbull",
            "chips",
            "wine",
            "icecream",
            "redbull",
            "chips",
            "wine",
            "icecream",
        ],
        "amount": [45, 60, 60, 45, 100, 140, 190, 170, 55, 70, 20, 45],
    }
    df_stores_north = pd.DataFrame(data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS df_stores_north AS SELECT * FROM df_stores_north"
    )

    # Population table
    datapop = {
        "year": [2016, 2017, 2018, 2019, 2020] * 3,
        "region": (["IDF"] * 5) + (["HDF"] * 5) + (["PACA"] * 5),
        "population": [1010000, 1020000, 1030000, 1040000, 1000000]
        + [910000, 920000, 930000, 940000, 900000]
        + [810000, 820000, 830000, 840000, 950000],
    }
    dfpop = pd.DataFrame(datapop)
    con.execute("CREATE TABLE IF NOT EXISTS dfpop AS SELECT * FROM dfpop")

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
        df = pd.read_excel(
            "data/08_grouping_sets/estim-pop-dep-sexe-gca-1975-2023.xls",
            str(year),
            skiprows=3,
        )
        subset = df[df["Départements"].isin(["59", "62", "75", "95", "83", "84"])][
            ["Départements", "Unnamed: 7"]
        ]
        subset["year"] = year
        dpts_dfs.append(subset)

    dpts_dfs = pd.concat(dpts_dfs)
    dpts_dfs.columns = ["departement", "population", "year"]
    dpts_dfs["region"] = dpts_dfs["departement"].apply(
        lambda x: dpt_to_region_mapping.get(x)
    )

    dpts_dfs = dpts_dfs[["region", "departement", "year", "population"]]
    con.execute("CREATE TABLE IF NOT EXISTS dpts_dfs AS SELECT * FROM dpts_dfs")

    # Dataframe for ROLLUP & CUBE
    # Data assurance soin
    df_assurance_soins = pd.read_csv("data/08_grouping_sets/data_assurance_soins.csv")
    con.execute(
        "CREATE TABLE IF NOT EXISTS df_assurance_soins AS SELECT * FROM df_assurance_soins"
    )

    exercises_and_questions = [
        {
            "exercise_name": "ex01A_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Le commercial d'une marque de boisson énergisante veut savoir quel est le magasin de notre "
            "enseigne qui vend le plus de son produit.",
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
            "produit (SUM + groupby)",
        },
        {
            "exercise_name": "ex01C_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Faites un GROUPING SETS, pour grouper par plusieurs niveaux d'agrégation",
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
            "6) Filtrez sur table_de_gauche.product_name = 'redbull' et table_de_droite.product_name IS NULL\n",
        },
        {
            "exercise_name": "ex02_grouping_sets_dfpop",
            "tables": ["dfpop"],
            "question": "Grouper la population par : \n"
            "- année et région\n"
            "- année seulement\n",
        },
        {
            "exercise_name": "ex03A_grouping_sets_dpts_dfs",
            "tables": ["dpts_dfs"],
            "question": "Grouping sets sur données de population réelle. \n"
            "Grouper la population par : \n"
            "- année et région\n"
            "- année seulement\n",
        },
        {
            "exercise_name": "ex01E_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Utiliser FILTER afin de trouver les magasins qui ont vendu le plus grand nombre de redbull "
            "en proportion de leur C.A.\n"
            "On doit trouver le même résultat que l'exercice 01B",
        },
        {
            "exercise_name": "ex01F_grouping_sets_df_redbull",
            "tables": ["df_stores_north"],
            "question": "Utiliser cette fois-ci un CASE WHEN  afin de trouver les magasins qui ont vendu le plus grand "
            "nombre de redbull en proportion de leur C.A.\n"
            "FILTER n'existe pas partout. La bonne nouvelle, c'est qu'on peut imiter son fonctionnement "
            "avec CASE WHEN!\n"
            "On doit trouver le même résultat que l'exercice 01B",
        },
        {
            "exercise_name": "ex03B_grouping_sets_dpts_dfs",
            "tables": ["dpts_dfs"],
            "question": "Utilisez une agrégation couplée avec un FILTER pour avoir, pour chaque année, la population "
            "de la region IDF en face du total pour calculer la part de la pop IDF sur le total",
        },
        {
            "exercise_name": "ex03C_grouping_sets_dpts_dfs",
            "tables": ["dpts_dfs"],
            "question": "Utilisez une agrégation couplée avec un CASE WHEN pour avoir, pour chaque année, la population "
            "de la region IDF en face du total pour calculer la part de la pop IDF sur le total",
        },
        {
            "exercise_name": "ex04A_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Votre PO vous demande le montant total remboursé par type de contrat",
        },
        {
            "exercise_name": "ex04B_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Votre PO vous demande le montant total remboursé par type de contrat et par type d'acte",
        },
        {
            "exercise_name": "ex04C_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Le PO revient en râlant : le manager n'avait rien compris ! Il veut le montant total remboursé "
            "par type de contrat et le montant total remboursé par type d'acte\n"
            "Hint: commencez simple, faites le avec un Union",
        },
        {
            "exercise_name": "ex04D_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Votre tech lead vient vous voir : 'Ton code fait le taff, mais j'ai récemment lu un"
            " article sur les GROUPING SETS, je pense que ça permettrait de simplifier le code sur ton "
            "problème, tu peux implémenter ça? Merci!'",
        },
        {
            "exercise_name": "ex04E_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Votre manager revient à la charge : 'Perso, je trouve que c'était très bien d'avoir aussi le "
            "montant total remboursé par type de contrat et par type d'acte.\n "
            "J'ai discuté avec le PO et il est OK. Garde ce que t'as fait, mais remets aussi les subdivisions\n"
            "Vous décidez d'utiliser ROLLUP pour obtenir tout ça facilement :",
        },
        {
            "exercise_name": "ex04F_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "Votre tech lead vérifie votre code et vous dit : 'Tu t'es planté. ROLLUP ça enlève "
            "progressivement le niveau de regroupement le plus à droite de ta liste. Résultat : on n'a pas "
            "les sommes par type_acte uniquement (il manque 5 lignes). Il faut trouver une autre solution!\n"
            "Il nous faut donc :\n "
            "- la somme par type d'acte (5 lignes),\n"
            "- la somme par type de contrat (5 lignes),\n"
            "- ET la somme par type d'acte + type de contrat (25 lignes),\n\n"
            "Et effectivement, avec ROLLUP il nous manquait la somme par type d'acte uniquement (5 lignes)\n"
            "Vous décidez d'utiliser un CUBE Pour avoir toutes les options: ",
        },
        {
            "exercise_name": "ex04G_grouping_sets_df_assurance_soins",
            "tables": ["df_assurance_soins"],
            "question": "En lisant le rapport fourni par votre P.O. sur la base de vos chiffres <br />  Votre N+2 a "
            "eu plein d'idées.\n"
            "'Je veux la somme des montants remboursés par : type_contrat / type_acte / groupe_age / sexe / annee"
            " et je veux avoir les chiffres globaux pour chacune de ces sous-catégories :'\n"
            "- type_contrat / type_acte / groupe_age / sexe /\n"
            "- type_contrat / type_acte / groupe_age /\n"
            "- type_contrat / type_acte / \n"
            "- type_contrat /\n\n "
            "Maintenant que vous connaissez ROLLUP, ça devrait être un jeu d'enfant :",
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
                  INSERT OR IGNORE INTO memory_state (theme, exercise_name, tables, last_reviewed)
                  VALUES (
                      '08_grouping_sets',
                       '{exercise_name}',
                       '{tables}',
                       '{date.today()}'
                       )
                  """
        )
