import sqlite3
import os

def run_query(sql_query):
    
    try:
        base_dir = os.path.dirname(__file__)
        db_path = os.path.join(base_dir, "chinook.db")
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()

        cursor.execute(sql_query)
        rows=cursor.fetchall()

        column_names=[desc[0] for desc in cursor.description]

        conn.close()

        return [dict(zip(column_names,row)) for row in rows]
    
    except Exception as e:
        return f"Error executing sql:{str(e)}"