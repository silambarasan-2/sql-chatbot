import sqlite3

def extract_schema(db_path="main/chinook.db"):
    try:
        conn = sqlite3.connect(db_path)              # 1. Connect to the database
        cursor = conn.cursor()                       # 2. Create a cursor to run SQL

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()                   # 3. Get all table names

        schema = []                                  # 4. To hold schema descriptions

        for table in tables:                         # 5. Loop through each table
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()              # 6. Get column info for the table
            column_names = [col[1] for col in columns]  # col[1] is the column name
            schema.append(f"{table_name} has columns: {', '.join(column_names)}")

        conn.close()                                 # 7. Close the database connection

        return "\n".join(schema)                     # 8. Return schema info as a string

    except Exception as e:
        return f"Error extracting schema: {str(e)}"  # 9. If error occurs, return message
