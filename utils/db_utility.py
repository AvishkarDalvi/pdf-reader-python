import sys
import mysql.connector
from utils.config_utility import load_config

def connect_database():
    """
    Connect to the configured MySQL database.

    Returns:
        A MySQL connection object.

    Exits:
        The program exits if the database connection cannot be established.
    """
    config = load_config()

    try:
        connection = mysql.connector.connect(
            host=config["db_host"],
            user=config["db_user"],
            password=config["db_password"],
            database=config["db_name"],
        )
        if connection.is_connected():
            print("Connected to MySQL")

        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)
        
def create_questions_table(connection):
    """
    Create the 'questions' table in the database if it does not exist.

    Exits:
        The program exits if the table creation fails.
    """
    cursor = connection.cursor()
    try:
        create_questions_table_query = """
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                subject VARCHAR(255),
                chapter VARCHAR(255),
                question TEXT,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                option_d TEXT,
                answer TEXT
            );
        """
        cursor.execute(create_questions_table_query)
        connection.commit()
        print("Table 'questions' is ready.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        sys.exit(1)
    finally:
        cursor.close()
        
def insert_question(connection, question_data):
    """
    Insert a question into the 'questions' table.

    Args:
        connection: The MySQL connection object.
        question_data: A dictionary containing question details.

    Exits:
        The program exits if the insertion fails.
    """
    cursor = connection.cursor()
    try:
        option_a, option_b, option_c, option_d = question_data["options"]
        insert_query = """
            INSERT INTO questions (subject, chapter, question, option_a, option_b, option_c, option_d, answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            question_data["subject"],
            question_data["chapter"],
            question_data["question"],
            option_a,
            option_b,
            option_c,
            option_d,
            question_data["answer"]
        ))
        connection.commit()
        print("Question inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting question: {err}")
        sys.exit(1)
    finally:
        cursor.close()
        
def fetch_questions_by_chapter(chapter_name, connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM questions WHERE chapter = %s", (chapter_name,))
        questions = cursor.fetchall()
        return questions
    except mysql.connector.Error as err:
        print(f"Error fetching questions: {err}")
        sys.exit(1)
    finally:
        cursor.close()
        
def close_database(connection):
    """
    Close the database connection.

    Args:
        connection: The MySQL connection object.
    """
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")