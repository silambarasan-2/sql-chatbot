# main/sql_generator.py

import requests
import os
import re

def load_system_prompt():
    """Loads the system prompt containing schema and instructions."""
    base_dir = os.path.dirname(__file__)  # This points to the 'main' folder
    prompt_path = os.path.join(base_dir, "system_prompt.txt")
    
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()
    

def clean_sql(sql_text):
    import re

    # Remove markdown ticks and comments
    sql_text = re.sub(r"```(?:sql)?", "", sql_text, flags=re.IGNORECASE).strip("` \n")
    sql_text = re.sub(r"--.*", "", sql_text)

    # Combine lines and remove extra semicolons
    lines = [line.strip() for line in sql_text.splitlines() if line.strip()]
    combined = " ".join(lines)
    combined = combined.replace(" ;", ";")  # fix spacing issue

    # Remove all semicolons except at the end of the final query
    combined = re.sub(r";+", "", combined).strip()
    return combined + ";"



    

def generate_sql(user_input):
    """
    Sends a prompt to the locally running Mistral model via Ollama
    and returns the cleaned SQL query.
    """
    system_prompt = load_system_prompt()
    
    full_prompt = f"""{system_prompt}

User question: {user_input}

Only return a single SQL query with correct singular and case-sensitive table names from the Chinook database. Do not pluralize any table names. Do not add explanations, markdown, or comments.

Respond ONLY with one valid SQL query using correct table and column names from the Chinook database.
DO NOT include explanations, markdown (```), comments (--), or multiple queries.
Only return the SQL query in one line if possible.

Do not use markdown formatting, comments, or placeholders like <Number_of_results>.
Always return executable SQL queries with real values (e.g., LIMIT 5).

Always use actual values — never use placeholders like <Number_of_results>.

SQL Query:"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        raw_sql = response.json()["response"]

        # Clean up the generated SQL (remove markdown ticks if present)
        cleaned_sql = clean_sql(raw_sql)

        return cleaned_sql
    except Exception as e:
        return f"Error generating sql: {str(e)}"
