# tasks.py

import mysql.connector
from celery import Celery
from datetime import datetime


from celeryconfig import app


db_config = {
    'user': 'root',
    'password': '#Likithxlr8',
    'host': 'localhost',
    'database': 'new_articles'
}


@app.task
def insert_article(title, content, url, published_date_str):
    try:
        
        published_date = datetime.strptime(published_date_str, '%Y-%m-%d %H:%M:%S')
        
       
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        
        query = """
        INSERT INTO articles_preprocessing (title, content, url, published_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (title, content, url, published_date)
        
        
        cursor.execute(query, data)
        
        
        conn.commit()
        
        print(f"Article '{title}' inserted successfully.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        
        if cursor:
            cursor.close()
        if conn:
            conn.close()
