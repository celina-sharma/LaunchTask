import autogen
import sqlite3
import csv

# LLM Config
config_list = [
    {
        "model": "mistral",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.3,
}

def create_database_from_csv():
    """
    Creates sales.db from sales.csv file
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            category TEXT,
            amount REAL,
            quantity INTEGER,
            total_price REAL,
            region TEXT,
            payment_method TEXT,
            date TEXT
        )
    """)
    
    # Read from sales.csv and insert into database
    with open("sales.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute("""
                INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["id"],
                row["product"],
                row["category"],
                row["amount"],
                row["quantity"],
                row["total_price"],
                row["region"],
                row["payment_method"],
                row["date"]
            ))
    
    conn.commit()
    conn.close()
    print("Database created from sales.csv!")

# Tool Function
def query_database(sql: str) -> str:
    """
    Executes SQL query on SQLite database and returns results
    """
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return f"Columns: {columns}\nResults: {results}"
    except Exception as e:
        return f"Database Error: {str(e)}"

# DB Agent
db_agent = autogen.AssistantAgent(
    name="DBAgent",
    system_message="""
    You are a DB Agent. You can query a SQLite database using the query_database tool.
    
    The database has a table called 'sales' with these columns:
    - id (INTEGER)
    - product (TEXT)
    - category (TEXT)
    - amount (REAL)
    - quantity (INTEGER)
    - total_price (REAL)
    - region (TEXT)
    - payment_method (TEXT)
    - date (TEXT)
    
    Rules:
    - Use query_database tool to answer data questions
    - Always use correct column names from the table above
    - Write correct SQL queries
    - Always include the column name in SELECT when using GROUP BY
    - Present results clearly
    - Keep responses under 100 words
    - End your message with: "DB_QUERY_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("DB Agent loaded successfully")
    print(f"Agent Name: {db_agent.name}")
    print(f"Tool: SQLite + SQL")
    
    # User Proxy for individual testing
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        code_execution_config=False,
    )
    
    # Register tool
    autogen.register_function(
        query_database,
        caller=db_agent,
        executor=user_proxy,
        name="query_database",
        description="Executes SQL query on SQLite database and returns results"
    )
    
    create_database_from_csv()
    
    # Test the agent
    user_proxy.initiate_chat(
        db_agent,
        message="Show me total sales by region"
    )