import autogen
import sys
sys.path.append('./tools')

from code_executor import code_agent, run_python_code
from db_agent import db_agent, query_database, create_database_from_csv
from file_agent import file_agent, read_csv, write_txt

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
    "timeout": 300,
}

# Orchestrator
orchestrator = autogen.AssistantAgent(
    name="Orchestrator",
    system_message="""
    You are an Orchestrator. You receive user requests and assign tasks to the right agents.
    
    You have these agents available:
    - FileAgent: reads CSV files and writes TXT files
    - CodeAgent: executes Python code for analysis
    
    Your job:
    1. Receive the user request
    2. Assign FileAgent to read sales.csv
    3. Assign CodeAgent to analyze the data and generate insights
    4. Combine results into a final answer
    
    Rules:
    - Keep responses clear and concise
    - End with: "ORCHESTRATION_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

# User Proxy
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
)

# Register all tools
autogen.register_function(
    read_csv,
    caller=file_agent,
    executor=user_proxy,
    name="read_csv",
    description="Reads a CSV file and returns its contents"
)

autogen.register_function(
    write_txt,
    caller=file_agent,
    executor=user_proxy,
    name="write_txt",
    description="Writes content to a TXT file"
)

autogen.register_function(
    run_python_code,
    caller=code_agent,
    executor=user_proxy,
    name="run_python_code",
    description="Executes Python code and returns the output"
)

autogen.register_function(
    query_database,
    caller=db_agent,
    executor=user_proxy,
    name="query_database",
    description="Executes SQL query on SQLite database and returns results"
)

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Tool-Chain Pipeline - Day 3")
    print("Flow: User -> Orchestrator -> File Agent -> Code Agent -> Final Answer")
    print("=" * 60)

    # Create database from sales.csv
    create_database_from_csv()

    # Step 1: Orchestrator receives user request
    print("\nSTEP 1: Orchestrator planning tasks...")
    user_proxy.initiate_chat(
        orchestrator,
        message="Analyze sales.csv and generate top 5 insights"
    )

    # Step 2: File Agent reads sales.csv
    print("\nSTEP 2: File Agent reading sales.csv...")
    user_proxy.initiate_chat(
        file_agent,
        message="Read the sales.csv file and return column names and total row count only"
    )

    # Step 3: Code Agent analyzes data and generates insights
    print("\nSTEP 3: Code Agent generating top 5 insights...")
    user_proxy.initiate_chat(
        code_agent,
        message="""
        Write and execute Python code that:
        1. Reads sales.csv using pandas
        2. Generates these 5 insights:
           - Top selling product by total_price
           - Region with highest total sales
           - Most used payment method
           - Best selling month
           - Top selling category
        3. Prints each insight clearly
        """
    )

    # Get code output
    code_output = user_proxy.chat_messages[code_agent][-1]['content']

    # Step 4: File Agent saves insights
    print("\nSTEP 4: Saving insights to insights.txt...")
    user_proxy.initiate_chat(
        file_agent,
        message=f"Write this content to a file called 'insights.txt':\n{code_output}"
    )

    print("\n" + "=" * 60)
    print("Pipeline Complete! Check insights.txt for results")
    print("=" * 60)