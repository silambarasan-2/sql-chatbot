from sql_generator import generate_sql

query=generate_sql("list albumid in album")
print("Generated SQL:\n",query)