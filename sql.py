from dotenv import load_dotenv
load_dotenv()## load all environment variables from .env file
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## configure AI key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## function to load google gemini model  and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function to retrieve query results from the database
def read_sql_query(sql,db):
    conn= sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    for row in rows:
        print(row)
    return rows

## define your prompt
prompt=[
    """
    You are an expert in converting English questions to SQL code
    The SQL database has the name STUDENT and has the following columns:
    NAME, CLASS, SECTION.\n\n For Example,\nExample 1- How many entriees of records are presnet?,
    the SQL command will be something like this:
    SELECT COUNT(*) FROM STUDENT; also the sql code should not have ''' in beginning or end and sql word in output
    \nExample 2- Tell me all thbe students studying in CSE section?,
    the SQL command will be something like this:
    SELECT * FROM STUDENT WHERE SECTION='CSE'; also the sql code should not have ''' in beginning or end and sql word in output
    """
]

## streamlit app
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App to Retrieve SQL data")

question=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

# if submit is clicked 
if submit:
    if question:
        # get the response from gemini
        response=get_gemini_response(question,prompt)
        print("Response from Gemini:", response)
        response=read_sql_query(response,'student.db')
        st.subheader("Response from Gemini:")
        for row in response:
            print(row)
            st.header(row)
