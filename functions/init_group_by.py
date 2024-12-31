import pandas as pd


def init_group_by(con):
    """

    :param con:
    :return:
    """
    appt_nord = pd.read_csv("data/06_group_by/appartements_nord_pdc.csv")
    con.execute("CREATE TABLE IF NOT EXISTS appt_nord AS SELECT * FROM appt_nord")

    # Nombre de ventes par commune
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex01_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # La moyenne des prix par commune
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex02_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Moyenne et count du nombre de lignes
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex03_group_by_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et subquery
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex04_where_and_subquery_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et CTE
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex05_where_and_CTE_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )

    # Where et having
    con.execute(
        """
        INSERT INTO memory_state (theme, exercise_name, tables, last_reviewed)
        VALUES (
            '06_group_by',
             'ex06_where_and_having_appt_nord',
             '["appt_nord"]',
             '1970-01-01'
             )
        """
    )
