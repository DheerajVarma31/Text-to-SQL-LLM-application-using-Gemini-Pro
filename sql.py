import sqlite3
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# Load environment variables from .env
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Gemini and generate SQL
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")  # Use a valid model
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to execute SQL on SQLite DB
def execute_sql_query(sql_query, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.commit()
        conn.close()
        return rows, column_names
    except Exception as e:
        return str(e), []

# Prompt template to instruct the model
prompt = [
    """
    You are an expert SQL translator. Convert English questions to valid SQL queries.
    The table name is STUDENT and it contains columns: NAME, CLASS, SECTION.

    Output should ONLY be the SQL query without explanation or any code formatting (no ```sql).
    Examples:

    Q: How many students are in the database?
    A: SELECT COUNT(*) FROM STUDENT;

    Q: List students in the CSE section.
    A: SELECT * FROM STUDENT WHERE SECTION = 'CSE';
    """
]

# Streamlit UI
st.set_page_config(page_title="🧠 Gemini + SQL Query App")
st.title("🧠 Gemini + SQL Query App")
st.markdown("Ask a natural language question, and I'll query the database for you!")

# User input
question = st.text_input("Your Question:")
submit = st.button("Generate SQL & Run")

if submit and question:
    sql_query = get_gemini_response(question, prompt)
    
    st.subheader("🧾 Generated SQL Query:")
    st.code(sql_query, language='sql')

    # Execute SQL
    result, columns = execute_sql_query(sql_query, "student.db")

    if isinstance(result, str):
        st.error(f"❌ Error: {result}")
    elif result:
        st.subheader("📊 Query Result:")
        df = pd.DataFrame(result, columns=columns)
        st.dataframe(df)
    else:
        st.info("✅ Query executed successfully, but no data was returned.")
