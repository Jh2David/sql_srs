SELECT Div,
    COUNT (
        CASE
            WHEN HomeTeam = 'Lille' AND FTHG > FTAG THEN 1
        END
    ) AS lille_wins_home,
    COUNT (
        CASE
            WHEN AwayTeam = 'Lille' AND FTHG < FTAG THEN 1
        END
    ) AS lille_wins_away
FROM df_foot
GROUP BY Div
