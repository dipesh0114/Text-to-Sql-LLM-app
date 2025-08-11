from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re

# Configure GenAI Key
genai.configure(api_key=os.getenv("Google_Api_Key"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to clean AI-generated SQL
def sanitize_sql(query: str) -> str:
    # Remove code block markers and "sql" labels
    query = re.sub(r"```sql|```", "", query, flags=re.IGNORECASE)
    # Remove phrases like "Here is the SQL query:"
    query = re.sub(r"(?i)here\s+is\s+the\s+sql\s+query:?", "", query)
    # Strip whitespace and semicolons at the ends
    return query.strip().rstrip(";")

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

    Example 1:
    Q: How many entries of records are present?
    A: SELECT COUNT(*) FROM STUDENT;

    Example 2:
    Q: Tell me all the students studying in Data Science class?
    A: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Only return the SQL code, no extra words, no ```sql``` blocks, no explanations.
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    raw_response = get_gemini_response(question, prompt)
    print("Raw model output:", raw_response)

    safe_query = sanitize_sql(raw_response)
    print("Sanitized SQL:", safe_query)

    try:
        rows = read_sql_query(safe_query, "student.db")
        st.subheader("The Response is:")
        for row in rows:
            print(row)
            st.header(row)
    except sqlite3.Error as e:
        st.error(f"SQL error: {e}")
