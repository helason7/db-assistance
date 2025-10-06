# Import our database tools
from db_tools import init_database, create_table, getAllDB, getTablesFromDB, getDataFromTable, delete_db_file
import streamlit as st
import os
import chatbot


def db_init():
    st.title("Database Settings")
    
    # Database initialization section
    st.header("Database Init")
    db_name = st.text_input('Masukan Nama Database', value='contoh: sample_sales', key='db_name')

    # Add a button to initialize the database
    init_db_button = st.button("Create Database", help="Create the database file")

    # Initialize database if button is clicked
    if init_db_button:
        with st.spinner("Initializing database..."):
            result = init_database(db_name + ".db")
            st.success(result)

    db_folder = os.path.join(os.path.dirname(__file__) or ".", "db")
    if not os.path.exists(db_folder):
        st.info("No 'db' folder found in the project.")
        return

    # Find all .db files
    db_files = [f for f in os.listdir(db_folder) if f.endswith('.db')]
    if not db_files:
        st.info("No .db files found in the 'db' folder.")
        return

    dbs = getAllDB(db_folder, db_files)
    st.write("### Databases")
    # Render a table with an action column (Delete)
    for r in dbs:
        cols = st.columns([3, 1, 1, 1])
        cols[0].write(f"**{r['filename']}**\n{r['size_kb']} KB | {r['tables']} tables")
        cols[1].write(r['path'])
        # Delete button with confirmation
        delete_key = f"delete_{r['filename']}"
        if cols[2].button("Delete", key=delete_key):
            st.session_state[f"confirm_{r['filename']}"] = True
        if st.session_state.get(f"confirm_{r['filename']}"):
            confirm_cols = st.columns([1, 1, 1])
            if confirm_cols[0].button("Confirm Delete", key=f"confirm_{r['filename']}_ok"):
                db_folder = os.path.join(os.path.dirname(__file__) or ".", "db")
                res = delete_db_file(db_folder, r['filename'])
                if res.get('ok'):
                    st.success(res.get('message'))
                    # clear the confirmation and attempt to rerun to refresh
                    st.session_state.pop(f"confirm_{r['filename']}", None)
                    # Compatibility: some Streamlit versions don't expose experimental_rerun
                    try:
                        st.experimental_rerun()
                    except AttributeError:
                        # Try known internal RerunException locations across versions
                        tried = False
                        for mod_path in (
                            "streamlit.runtime.scriptrunner.script_runner",
                            "streamlit.scriptrunner.script_runner",
                        ):
                            try:
                                module = __import__(mod_path, fromlist=["RerunException"]) 
                                RerunException = getattr(module, "RerunException")
                                raise RerunException()
                            except (ImportError, AttributeError, Exception):
                                continue
                        # Final fallback: stop the script (won't rerun automatically)
                        try:
                            st.stop()
                        except Exception:
                            pass
                else:
                    st.error(res.get('message'))
            if confirm_cols[1].button("Cancel", key=f"confirm_{r['filename']}_cancel"):
                st.session_state.pop(f"confirm_{r['filename']}", None)


def browseDB():
    st.title("Browse")
    
    db_folder = os.path.join(os.path.dirname(__file__) or ".", "db")
    db_files = [f for f in os.listdir(db_folder) if f.endswith('.db')]
    dbs = getAllDB(db_folder, db_files)
    # Let user select a database to inspect
    sel = st.selectbox("Select a database to inspect", [r['filename'] for r in dbs])
    
    st.header("Create Table from CSV")
    tb_name = st.text_input('Masukan Nama Table', value='contoh: tb_sales', key='tb_name')
    # File Uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Add a button to create the table
        create_tb_button = st.button("Create Table", help="Create table from uploaded CSV")

        # Create table if button is clicked
        if create_tb_button:
                with st.spinner("Creating table..."):
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    try:
                        create_table(sel, temp_path, tb_name)
                        st.success(f"Table '{tb_name}' created successfully!")

                        # Clean up temp file
                        os.remove(temp_path)

                        # Attempt to refresh the app so new table appears
                        try:
                            st.experimental_rerun()
                        except AttributeError:
                            for mod_path in (
                                "streamlit.runtime.scriptrunner.script_runner",
                                "streamlit.scriptrunner.script_runner",
                            ):
                                try:
                                    module = __import__(mod_path, fromlist=["RerunException"]) 
                                    RerunException = getattr(module, "RerunException")
                                    raise RerunException()
                                except (ImportError, AttributeError, Exception):
                                    continue
                        except Exception:
                            try:
                                st.stop()
                            except Exception:
                                pass
                    except Exception as e:
                        st.error(f"Error creating table: {str(e)}")
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

    if sel:
        sel_path = next(r['path'] for r in dbs if r['filename'] == sel)
        try:
            tables = getTablesFromDB(sel_path)
        except Exception as e:
            st.error(f"Error opening DB: {e}")
            return

        st.write(f"#### Tables in {sel}")
        if not tables:
            st.write("(no tables)")
            return

        tsel = st.selectbox("Select a table to preview", tables)
        if tsel:
            cols, data = getDataFromTable(sel_path, tsel)
            st.write(f"Preview of {tsel} (up to 20 rows)")
            if cols:
                import pandas as pd
                df = pd.DataFrame(data, columns=cols)
                st.dataframe(df)
            else:
                st.write("No columns to display.")



def run():
    # Create a sidebar section for app settings and page navigation
    pages = ["DB Settings", "Browse", "Others", "Chatbot"]

    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0

    with st.sidebar:
        # Prev / Next buttons
        # cols = st.columns([1, 1, 1])
        # if cols[0].button("Prev"):
        #     st.session_state.page_idx = max(0, st.session_state.page_idx - 1)
        # cols[1].markdown(f"**{pages[st.session_state.page_idx]}**")
        # if cols[2].button("Next"):
        #     st.session_state.page_idx = min(len(pages) - 1, st.session_state.page_idx + 1)

        st.markdown("---")
        st.header("Navigation")
        # Direct page buttons
        for i, p in enumerate(pages):
            if st.button(p):
                st.session_state.page_idx = i

    # Page dispatch
    if st.session_state.page_idx == 0:
        db_init()
    elif st.session_state.page_idx == 1:
        browseDB()
    elif st.session_state.page_idx == 2:
        browseDB()
    else:
        # Chatbot page
        try:
            chatbot.run()
        except Exception as e:
            st.error(f"Failed to launch chatbot: {e}")

# end of file




if __name__ == '__main__':
  run()