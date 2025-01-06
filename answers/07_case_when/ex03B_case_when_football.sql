SELECT Div,
    AVG (
        CASE
            WHEN data.HomeTeam = 'Lille' AND FTHG > FTAG THEN 1
            WHEN data.HomeTeam = 'Lille' AND FTHG <= FTAG THEN 0
        END
    ) AS lille_wins_home,
    AVG (
        CASE
            WHEN data.AwayTeam = 'Lille' AND FTHG < FTAG THEN 1
            WHEN data.AwayTeam = 'Lille' AND FTHG >= FTAG THEN 0
        END
    ) AS lille_wins_away,
FROM df_foot
GROUP BY Div
