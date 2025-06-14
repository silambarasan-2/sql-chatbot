import streamlit as st
from sql_generator import generate_sql
from db_connector import run_query
import pandas as pd

st.set_page_config(page_title="SQL Chatbot", layout="centered")

st.title("💬 Shield SQL Chatbot")
st.caption("Ask anything about the Chinook database (offline).")

user_input = st.text_input("Your Question:")

if st.button("Ask"):
    if not user_input:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL query..."):
            sql_query = generate_sql(user_input)
            st.code(sql_query, language='sql')

        with st.spinner("Running SQL query..."):
            results = run_query(sql_query)

        if isinstance(results, str):
            st.error(results)
        elif results:
            df = pd.DataFrame(results)
            st.success("Here are your results:")
            st.dataframe(df)
        else:
            st.info("No results found.")
