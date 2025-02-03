# 📘 SQL SRS - Apprends le SQL avec des Flashcards interactives ! 🎓

🎯 [Testez l'application en ligne ici ! 🚀](https://sqlsrs-jh2david.streamlit.app)

## 🚀 Description
Ce projet est une application interactive développée avec **Streamlit** qui permet de réviser les requêtes **SQL** sous forme de flashcards. L'objectif est de proposer une manière ludique et efficace d'apprendre et de s'entraîner sur SQL.

## 🛠 Technologies utilisées
- **Python**
- **Streamlit** (interface utilisateur interactive)
- **SQL** 



## 🔧 Installation et Exécution
1. Clonez ce repo :
   ```bash
   git clone https://github.com/Jh2David/sql_srs.git
   cd sql_srs
   ```
2. Installez les dépendances :
  ```bash
   pip install -r requirements.txt
  ```

3. Lancez l’application Streamlit :
  ```bash
   streamlit run app.py
  ```

## 🎯 Fonctionnement de l’application
	•	Un jeu de flashcards interactives s’affiche.
	•	L’utilisateur doit essayer de deviner la réponse à une requête SQL.
	•	En cliquant sur “Voir la réponse”, la requête correcte apparaît avec une explication.
	•	L’application permet ainsi d’apprendre SQL de façon ludique et interactive.

## 📚 Exemples de Flashcards SQL

| 🏷️ Question | 💡 Réponse |
|------------|----------|
| Sélectionner tous les utilisateurs | `SELECT * FROM users;` |
| Trouver le total des ventes par produit | `SELECT product, SUM(sales) FROM orders GROUP BY product;` |
| Afficher les clients ayant dépensé plus de 100€ | `SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id HAVING SUM(amount) > 100;` |
| Trouver le nombre total de commandes par jour | `SELECT DATE(order_date), COUNT(*) FROM orders GROUP BY DATE(order_date);` |
| Obtenir les trois produits les plus vendus | `SELECT product_id, COUNT(*) as sales FROM orders GROUP BY product_id ORDER BY sales DESC LIMIT 3;` |

## 🔥 Pourquoi ce projet ?

Ce projet a été développé dans le cadre de la formation Data Upskilling afin d’explorer les compétences en SQL et en développement d’applications interactives.
L’objectif était de concevoir un outil permettant de faciliter l’apprentissage des requêtes SQL de manière interactive et progressive.
L’implémentation a été réalisée en Streamlit, afin de proposer une interface simple et accessible, adaptée à un usage pédagogique.

## 🔜 Améliorations futures
	•	🔄 Mode aléatoire pour les flashcards.
	•	📊 Intégration avec BigQuery pour tester sur de vraies bases de données.
	•	🏆 Ajout d’un système de score pour suivre les progrès.
	•	🎨 Amélioration du design et de l’expérience utilisateur.

## 📌 Mots-clés
SQL, Flashcards, Data Engineer, Streamlit, Python, SQL Training
