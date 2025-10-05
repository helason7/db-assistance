# Database Builder Assistant

A comprehensive web application for database management and AI-powered SQL querying, built with Streamlit, SQLite, and Google Gemini AI.

## 🚀 Features

### Database Configuration
- **Database Initialization**: Create new SQLite database files
- **CSV Import**: Upload and import CSV files directly into database tables
- **Type Inference**: Automatic mapping of pandas data types to SQLite column types
- **Schema Generation**: Intelligent CREATE TABLE statement generation from DataFrames

### AI-Powered SQL Assistant
- **Natural Language Queries**: Ask questions about your data in plain English
- **Automatic SQL Generation**: AI generates and executes SQL queries based on your questions
- **Schema Understanding**: Built-in database schema exploration and sample data preview
- **Query Results**: Formatted display of SQL queries and their results

## 📋 Prerequisites

- Python 3.8 or higher
- Google AI API Key (for the chatbot feature)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd db-assistance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your Google AI API Key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Keep it secure and don't share it

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Database Configuration Page

1. **Initialize Database**:
   - Enter a database name (e.g., "sales_data")
   - Click "Initialize Database" to create the `.db` file

2. **Create Tables from CSV**:
   - Enter a table name
   - Upload a CSV file
   - Click "Create Table" to import the data

### Query Builder Assistant Page

1. **Setup**:
   - Enter your Google AI API Key in the sidebar
   - The AI assistant will automatically explore your database schema

2. **Ask Questions**:
   - Type natural language questions like:
     - "What are the top 5 products by sales?"
     - "How many customers do we have?"
     - "Show me sales data for the last month"
   - The AI will generate appropriate SQL queries and display results

## 📁 Project Structure

```
db-assistance/
├── app.py                      # Main Streamlit application
├── database_config.py          # Database configuration UI
├── chatbot.py                  # AI-powered SQL assistant
├── db_tools.py                 # Database utility functions
├── requirements.txt            # Python dependencies
├── README.md                   # This file
```

## 🔧 Key Functions

### db_tools.py
- `init_database(db_name)`: Initialize a new SQLite database file
- `create_table(db_name, csv_path, table_name)`: Create table from CSV with type inference
- `create_table_from_df(df, table_name, conn)`: Create table from pandas DataFrame
- `pandas_dtype_to_sqlite(dtype)`: Map pandas types to SQLite types
- `text_to_sql(sql_query)`: Execute SQL queries (used by AI assistant)

## 🎯 Type Mapping

The application automatically maps pandas data types to SQLite types:

| Pandas Type | SQLite Type |
|-------------|-------------|
| int64       | INTEGER     |
| float64     | REAL        |
| bool        | INTEGER     |
| datetime64  | TEXT        |
| object      | TEXT        |

## 🤖 AI Assistant Features

- **Schema Exploration**: Automatically analyzes database structure
- **Sample Data Preview**: Shows first 3 rows from each table
- **SQL Generation**: Creates complex queries with JOINs, aggregations, etc.
- **Error Handling**: Provides helpful error messages and query corrections
- **Query History**: Maintains conversation context

## 📊 Sample Data

The repository includes sample datasets:
- **Flight Data**: Aviation statistics and flight information
- **Video Game Sales**: Gaming industry sales data
- **Sales Database**: Pre-built SQLite database with sample sales data

## 🔒 Security Notes

- Keep your Google AI API key secure
- The application creates local SQLite files in the project directory
- No data is sent to external servers except for AI API calls

## 🐛 Troubleshooting

### Common Issues:

1. **"Invalid API Key" error**:
   - Verify your Google AI API key is correct
   - Check that you have access to Google AI services

2. **Database connection errors**:
   - Ensure the database file path is correct
   - Check file permissions

3. **CSV import issues**:
   - Verify CSV format (comma-separated, UTF-8 encoding)
   - Check for special characters in column names

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Uses [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph)
- SQLite for database management
- Pandas for data manipulation