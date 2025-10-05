import sqlite3
import pandas as pd
import os
from typing import List, Dict, Any, Optional

DB_PATH = ""

def init_database(db_name):
    global DB_PATH
    DB_PATH = db_name
    conn = sqlite3.connect(db_name)
    conn.close()

    return f"Database '{db_name}' berhasil dibuat."

def create_table(db_name, csv_path, table_name):
    # Baca file CSV
    df = pd.read_csv(csv_path)

    # Buat koneksi ke database SQLite
    conn = sqlite3.connect(db_name)

    # Masukkan data ke tabel
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Tutup koneksi
    conn.close()

    print(f"Table '{table_name}' berhasil dibuat.")

def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute an SQL query and return the results as a list of dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        # Set row_factory to sqlite3.Row to access columns by name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # Check if this is a SELECT query
        if query.strip().upper().startswith("SELECT"):
            # Fetch all rows and convert to list of dictionaries
            rows = cursor.fetchall()
            result = [{k: row[k] for k in row.keys()} for row in rows]
        else:
            # For non-SELECT queries, return affected row count
            result = [{"affected_rows": cursor.rowcount}]
            conn.commit()
            
        conn.close()
        return result
    
    except sqlite3.Error as e:
        return [{"error": str(e)}]
    
def get_table_schema() -> Dict[str, List[Dict[str, str]]]:
    """
    Get the schema of all tables in the database
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema = {}
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema[table_name] = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "pk": bool(col[5])
                }
                for col in columns
            ]
        
        conn.close()
        return schema
    
    except sqlite3.Error as e:
        return {"error": str(e)}

# Function to be used as a tool in the LangGraph agent
def text_to_sql(sql_query: str) -> Dict[str, Any]:
    """
    Execute a SQL query against the database
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Dictionary with SQL query and results
    """
    # Make sure the database exists
    if not os.path.exists(DB_PATH):
        init_database()
    
    # Execute the SQL query
    try:
        results = execute_sql_query(sql_query)
        return {
            "query": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "query": sql_query,
            "results": [{"error": str(e)}]
        }

def get_database_info() -> Dict[str, Any]:
    """
    Get information about the database schema to help with query construction
    
    Returns:
        Dictionary with database schema and sample data
    """
    # Make sure the database exists
    if not os.path.exists(DB_PATH):
        init_database()
    
    # Get the database schema
    schema = get_table_schema()
    
    # Get sample data for each table (first 3 rows)
    sample_data = {}
    for table_name in schema.keys():
        if isinstance(table_name, str):  # Skip any error entries
            try:
                sample_data[table_name] = execute_sql_query(f"SELECT * FROM {table_name} LIMIT 3")
            except:
                pass
    
    return {
        "schema": schema,
        "sample_data": sample_data
    }
