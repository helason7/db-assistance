import sqlite3
import pandas as pd
import os
from typing import List, Dict, Any, Optional, Tuple

DB_PATH = ""

def init_database(db_name):
    global DB_PATH
    DB_PATH = "db/" + db_name
    path = "db/" + db_name
    conn = sqlite3.connect(path)
    conn.close()

    return f"Database '{db_name}' berhasil dibuat."

def create_table(db_name, csv_path, table_name):
    # Baca file CSV
    df = pd.read_csv(csv_path)

    # Buat koneksi ke database SQLite
    path = "db/" + db_name
    conn = sqlite3.connect(path)

    # Masukkan data ke tabel
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Tutup koneksi
    conn.close()

    print(f"Table '{table_name}' berhasil dibuat.")

def execute_sql_query(query: str, db_path) -> List[Dict[str, Any]]:
    """
    Execute an SQL query and return the results as a list of dictionaries
    """
    try:
        path = "db/" + db_path
        conn = sqlite3.connect(path)
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
    
def get_table_schema(db_path) -> Dict[str, List[Dict[str, str]]]:
    """
    Get the schema of all tables in the database
    """
    try:
        path = "db/" + db_path
        conn = sqlite3.connect(path)
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
def text_to_sql(sql_query: str, db_path) -> Dict[str, Any]:
    """
    Execute a SQL query against the database
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Dictionary with SQL query and results
    """
    # # Make sure the database exists
    # if not os.path.exists(DB_PATH):
    #     init_database()
    
    # Execute the SQL query
    try:
        results = execute_sql_query(sql_query, db_path)
        return {
            "query": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "query": sql_query,
            "results": [{"error": str(e)}]
        }

def get_database_info(db_path) -> Dict[str, Any]:
    """
    Get information about the database schema to help with query construction
    
    Returns:
        Dictionary with database schema and sample data
    """
    # Make sure the database exists
    # if not os.path.exists(DB_PATH):
    #     init_database()
    
    # Get the database schema
    schema = get_table_schema(db_path)
    
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

def getAllDB(db_folder, db_files) -> List[dict]:
    
    # db_folder: filesystem path (str), db_files: list of filenames (List[str])
    # Build a table of metadata
    rows = []
    for fname in db_files:
        path = os.path.join(db_folder, fname)
        stat = os.stat(path)
        size_kb = stat.st_size / 1024
        mtime = stat.st_mtime

        # Count tables in the sqlite file
        try:
            import sqlite3
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
            table_count = cur.fetchone()[0]
            conn.close()
        except Exception:
            table_count = "error"

        rows.append({
            "filename": fname,
            "size_kb": round(size_kb, 1),
            "tables": table_count,
            "path": path,
        })
        
    return rows


def delete_db_file(db_folder: str, filename: str) -> dict:
    """
    Safely delete a database file from db_folder.

    Returns a dict with 'ok': bool and 'message': str.
    Safety checks:
    - filename must not contain path separators (prevents directory traversal)
    - file must exist inside db_folder
    """
    # Reject unsafe filenames
    if os.path.sep in filename or os.path.altsep and os.path.altsep in filename:
        return {"ok": False, "message": "Invalid filename"}

    path = os.path.join(db_folder, filename)

    # Normalize and ensure the file is inside the folder
    try:
        norm_folder = os.path.abspath(db_folder)
        norm_path = os.path.abspath(path)
    except Exception as e:
        return {"ok": False, "message": f"Invalid path: {e}"}

    if not norm_path.startswith(norm_folder):
        return {"ok": False, "message": "Invalid file location"}

    if not os.path.exists(norm_path):
        return {"ok": False, "message": "File does not exist"}

    try:
        os.remove(norm_path)
        return {"ok": True, "message": f"Deleted {filename}"}
    except Exception as e:
        return {"ok": False, "message": f"Error deleting file: {e}"}

def getTablesFromDB(sel_path) -> List[dict]:
    # if sel:
        # sel_path = next(r['path'] for r in rows if r['filename'] == sel)
        # sel_path = next(r['path'] for r in dbs if r['filename'] == sel)
    try:
        import sqlite3
        conn = sqlite3.connect(sel_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        f"Error opening DB: {e}"
        return
    
def getDataFromTable(sel_path, tsel) -> Tuple[List[str], List[tuple]]:
    try:
        conn = sqlite3.connect(sel_path)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tsel} LIMIT 20")
        cols = [d[0] for d in cur.description] if cur.description else []
        data = cur.fetchall()
        conn.close()
        return cols, data
    except Exception as e:
        f"Error opening DB: {e}"
        return [], []
    
