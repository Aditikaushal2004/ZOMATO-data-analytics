"""
Loads zomato_restaurants_data.csv into an embedded SQLite database (data/zomato.db)
and executes the 5 analytical SQL queries.
"""
import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "zomato_restaurants_data.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "zomato.db")
SQL_FILE = os.path.join(BASE_DIR, "sql", "02_zomato_queries.sql")

def run_zomato_sql():
    print(f"Reading CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.lower() for c in df.columns]

    print(f"Connecting to SQLite database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("restaurants", conn, if_exists="replace", index=False)
    
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_city ON restaurants(city);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cuisine ON restaurants(cuisine);")
    conn.commit()
    print("Database table 'restaurants' created successfully!\n")

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_text = f.read()

    queries = sql_text.split(";")
    query_num = 1
    
    for q in queries:
        clean_q = q.strip()
        if not clean_q or not any(kw in clean_q.upper() for kw in ["SELECT", "WITH"]):
            continue
            
        print("=" * 70)
        print(f"EXECUTING SQL QUERY {query_num}")
        print("=" * 70)
        res_df = pd.read_sql(clean_q, conn)
        print(res_df.to_string(index=False))
        print(f"(Rows returned: {len(res_df)})\n")
        query_num += 1

    conn.close()

if __name__ == "__main__":
    run_zomato_sql()
