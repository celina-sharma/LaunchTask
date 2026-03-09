import autogen
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

# Tool Function 1 — Read CSV file
def read_csv(filepath: str) -> str:
    """
    Reads a CSV file and returns its contents
    """
    try:
        with open(filepath, "r") as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            return f"Total rows: {len(rows)}\nColumns: {csv_reader.fieldnames}"
    except Exception as e:
        return f"File Error: {str(e)}"

# Tool Function 2 — Write to TXT file
def write_txt(filepath: str, content: str) -> str:
    """
    Writes content to a TXT file
    """
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return f"Successfully written to {filepath}"
    except Exception as e:
        return f"File Error: {str(e)}"

# File Agent
file_agent = autogen.AssistantAgent(
    name="FileAgent",
    system_message="""
    You are a File Agent. You can read CSV files and write TXT files.
    
    You have 2 tools:
    1. read_csv — reads a CSV file and returns its contents
    2. write_txt — writes content to a TXT file
    
    Rules:
    - Use read_csv tool to read CSV files
    - Use write_txt tool to save results
    - Present file contents clearly
    - Keep responses under 100 words
    - End your message with: "FILE_OPERATION_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("File Agent loaded successfully")
    print(f"Agent Name: {file_agent.name}")
    print(f"Tool: Read/write .txt, .csv")
    
    # User Proxy for individual testing
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        code_execution_config=False,
    )
    
    # Register tools
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
    
    # Test the agent
    user_proxy.initiate_chat(
        file_agent,
        message="Read the sales.csv file and tell me how many records it has"
    )