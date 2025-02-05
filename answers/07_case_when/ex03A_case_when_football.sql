SELECT Div,
    COUNT (
        CASE
            WHEN data.HomeTeam = 'Lille' AND FTHG > FTAG THEN 1
        END
    ) AS lille_wins_home,
    COUNT (
        CASE
            WHEN data.AwayTeam = 'Lille' AND FTHG < FTAG THEN 1
        END
    ) AS lille_wins_away,
FROM df_foot
GROUP BY Div
