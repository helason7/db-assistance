# Import our database tools
from db_tools import init_database, create_table
import streamlit as st
import os

def run():
    st.title("Database Configuration Tool")

    # Database initialization section
    st.header("1. Initialize Database")
    db_name = st.text_input('Masukan Nama Database', value='contoh: sample_sales', key='db_name')

    # Add a button to initialize the database
    init_db_button = st.button("Initialize Database", help="Create the database file")

    # Initialize database if button is clicked
    if init_db_button:
        with st.spinner("Initializing database..."):
            result = init_database(db_name + ".db")
            st.success(result)

    # Table creation section (only show if database is initialized)
    if init_db_button or os.path.exists(db_name + ".db"):
        st.header("2. Create Table from CSV")

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
                        create_table(db_name + ".db", temp_path, tb_name)
                        st.success(f"Table '{tb_name}' created successfully!")

                        # Clean up temp file
                        os.remove(temp_path)
                    except Exception as e:
                        st.error(f"Error creating table: {str(e)}")
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)




if __name__ == '__main__':
  run()