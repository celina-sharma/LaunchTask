import autogen
import subprocess
import sys

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

# Tool Function
def run_python_code(code: str) -> str:
    """
    Executes Python code and returns the output
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return f"Output:\n{result.stdout}"
        else:
            return f"Error:\n{result.stderr}"
    except Exception as e:
        return f"Execution Error: {str(e)}"

# Code Agent
code_agent = autogen.AssistantAgent(
    name="CodeAgent",
    system_message="""
    You are a Code Agent. You can execute Python code using the run_python_code tool.
    
    Rules:
    - When asked to perform calculations or analysis, write and execute Python code
    - Always use the run_python_code tool to execute code
    - Show the code you are running
    - Report the output clearly
    - Keep responses under 100 words
    - End your message with: "CODE_EXECUTION_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Code Agent loaded successfully")
    print(f"Agent Name: {code_agent.name}")
    print(f"Tool: Python execution")
    
    # User Proxy for individual testing
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        code_execution_config=False,
    )
    
    # Register tool
    autogen.register_function(
        run_python_code,
        caller=code_agent,
        executor=user_proxy,
        name="run_python_code",
        description="Executes Python code and returns the output"
    )
    
    # Test the agent
    user_proxy.initiate_chat(
        code_agent,
        message="Calculate the sum of numbers from 1 to 10 using Python code"
    )