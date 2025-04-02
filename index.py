from flask import Flask, request, jsonify, render_template
import psycopg2
import logging

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    conn = psycopg2.connect(
        database="user_db",
        user="root",
        host="db",
        password="lgedv2024"
    )
    return conn

with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL
            )
        """)
        conn.commit()

@app.route('/user', methods=['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        name = request.args.get('name')
        logging.info(f"GET request received for user with name: {name}")
        
        conn = get_db_connection()
        conn.autocommit = True  # Bật autocommit
        cur = conn.cursor()
        
        query = f"SELECT * FROM users WHERE name='{name}'"
        logging.info(f"Executing query: {query}")
        cur.execute(query)
        
        users = cur.fetchall()
        
        logging.info(f"Query executed successfully. Found {len(users)} users.")
        
        cur.close()
        conn.close()
        
        return render_template("user.html", users=users)
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        
        logging.info(f"POST request received. Adding user with name: {name}, age: {age}")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        insert_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
        logging.info(f"Executing query: {insert_query} with values ({name}, {age})")
        cur.execute(insert_query, (name, age))
        
        conn.commit()
        
        logging.info("User added successfully.")
        
        cur.close()
        conn.close()
        
        return render_template("user.html", message="User added successfully")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
