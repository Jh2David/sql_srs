# 📘 SQL SRS - Learn SQL with Interactive Flashcards! 🎓

🎯 [Try the online application here! 🚀](https://sqlsrs-jh2david.streamlit.app)

## 🚀 Description
This project is an interactive application built with **Streamlit** that allows you to review **SQL** queries in the form of flashcards. The goal is to provide a fun and effective way to learn and practice SQL.

## 🛠 Technologies Used
- **Python**
- **Streamlit** (interactive user interface)
- **SQL**

## 🔧 Installation and Execution
1. Clone this repo:
   ```bash
   git clone https://github.com/Jh2David/sql_srs.git
   cd sql_srs
   ```

2. Install the dependencies :
  ```bash
   pip install -r requirements.txt
  ```

3. Run the Streamlit application :
  ```bash
   streamlit run app.py
  ```

## 🎯 How the Application Works
	• A set of interactive flashcards is displayed.  
	• The user tries to guess the answer to an SQL query.  
	• By clicking on “Show Answer,” the correct query appears with an explanation.  
	• The application thus provides a fun and interactive way to learn SQL.  

 

## 📚 SQL Flashcard Examples

| 🏷️ Question | 💡 Answer |
|------------|----------|
| Select all users | `SELECT * FROM users;` |
| Find the total sales by product | `SELECT product, SUM(sales) FROM orders GROUP BY product;` |
| Display customers who spent more than 100€ | `SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id HAVING SUM(amount) > 100;` |
| Find the total number of orders per day | `SELECT DATE(order_date), COUNT(*) FROM orders GROUP BY DATE(order_date);` |
| Get the top three best-selling products | `SELECT product_id, COUNT(*) as sales FROM orders GROUP BY product_id ORDER BY sales DESC LIMIT 3;` |

## 🔥 Why this project ?

This project was developed as part of a Data Upskilling program to explore SQL skills and interactive application development.
The goal was to design a tool that facilitates learning SQL queries in an interactive and incremental way.
The implementation was done using Streamlit to provide a simple and accessible interface, suitable for educational use.

## 🔜 Future improvements
	• 🔄 Random mode for the flashcards.  
	• 🏆 Adding a scoring system to track progress.  
	• 🎨 Improving design and user experience.  

## 📌 Keywords
SQL, Flashcards, Data Engineer, Streamlit, Python, SQL Training
