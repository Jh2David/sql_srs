SELECT Div,
    AVG (
        CASE
            WHEN HomeTeam = 'Lille' AND FTHG > FTAG THEN 1
            WHEN HomeTeam = 'Lille' AND FTHG <= FTAG THEN 0
        END
    ) AS lille_wins_home,
    AVG (
        CASE
            WHEN AwayTeam = 'Lille' AND FTHG < FTAG THEN 1
            WHEN AwayTeam = 'Lille' AND FTHG >= FTAG THEN 0
        END
    ) AS lille_wins_away
FROM df_foot
GROUP BY Div
