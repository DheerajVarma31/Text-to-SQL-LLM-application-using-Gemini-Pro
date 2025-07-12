import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt instructions for Gemini
prompt_template = """
You are an expert at translating natural language to SQL.
You are working with a table called STUDENT with the following columns:
- NAME
- CLASS
- SECTION

Examples:
Q: How many students are there?
A: SELECT COUNT(*) FROM STUDENT;

Q: Show all students from CSE section.
A: SELECT * FROM STUDENT WHERE SECTION = 'CSE';

Q: Show students from class 3A
A: SELECT * FROM STUDENT WHERE CLASS = '3A';

Please return only the SQL query.
"""

def get_gemini_response(question: str) -> str:
    model = genai.GenerativeModel("gemini-pro")
    full_prompt = f"{prompt_template}\n\nQ: {question}\nA:"
    response = model.generate_content(full_prompt)
    return response.text.strip()

def run_query(query: str, db_path: str = "student.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [description[0] for description in cursor.description]
    conn.close()
    return col_names, rows

# Streamlit App UI
st.set_page_config(page_title="🧠 Gemini + SQL Query App")
st.title("🧠 Gemini + SQL Query App")
st.markdown("Ask a natural language question, and I'll query the database for you!")

question = st.text_input("Your Question:")
if st.button("Submit"):
    if question:
        try:
            sql_query = get_gemini_response(question)
            st.code(sql_query, language="sql")

            cols, result = run_query(sql_query)
            st.success("Query executed successfully!")
            st.dataframe(result, use_container_width=True, columns=cols)
        except Exception as e:
            st.error(f"Error: {e}")
