import duckdb
from functions.init_cross_joins import init_cross_joins
# from functions.init_inner_joins import init_inner_joins

# Connexion à DuckDB
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Initialisation des exercices
init_cross_joins(con)
# init_inner_joins(con)
# Appelle des fonctions pour d'autres jointures...

con.close()