from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Gemini and get SQL from a natural language question
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(model_name="gemini-pro")
    full_prompt = prompt[0] + "\n\nQuestion: " + question
    response = model.generate_content(full_prompt)
    return response.text.strip()

# Function to execute SQL query and return results
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return [("SQL Error", str(e))]

# Prompt for Gemini
prompt = [
    """
    You are an expert in converting English questions to SQL code.
    The SQL database is named STUDENT and has the following columns:
    NAME, CLASS, SECTION.

    Example 1:
    Question - How many entries of records are present?
    SQL - SELECT COUNT(*) FROM STUDENT;

    Example 2:
    Question - Tell me all the students studying in CSE section?
    SQL - SELECT * FROM STUDENT WHERE SECTION='CSE';

    Please only return the SQL code without explanations, no ```sql or other wrappers.
    """
]

# Streamlit UI
st.set_page_config(page_title="SQL Query Generator")
st.title("🧠 Gemini + SQL Query App")
st.write("Ask a natural language question, and I'll query the database for you!")

question = st.text_input("Your Question:")
submit = st.button("Submit")

if submit and question:
    with st.spinner("Generating SQL query..."):
        sql_query = get_gemini_response(question, prompt)
        st.code(sql_query, language="sql")

    with st.spinner("Fetching data from database..."):
        result_rows = read_sql_query(sql_query, "student.db")

    st.subheader("Results:")
    if result_rows:
        for row in result_rows:
            st.write(row)
    else:
        st.warning("No results found or invalid query.")
