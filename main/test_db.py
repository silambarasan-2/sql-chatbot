# test_db.py

from db_connector import run_query

sql = "Show 10 artists"
results = run_query(sql)

print("Query Results:")
if isinstance(results, str):
    print("SHIELD:", results)  # It's an error message
else:
    for row in results:
        print(row['FirstName'], "|", row['Email'])
