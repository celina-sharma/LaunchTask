import autogen
import threading
import sys
sys.path.append('./orchestrator')
sys.path.append('./agents')

from planner import planner
from worker_agent import worker1, worker2, worker3
from reflection_agent import reflection_agent
from validator import validator

# LLM Config
config_list = [
    {
        "model": "phi3",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama"
    }
]

# Store worker results
worker_results = {}

# Execution tree status
execution_tree = {
    "Orchestrator": "Running",
    "Worker1": "Running",
    "Worker2": "Running",
    "Worker3": "Running",
    "ReflectionAgent": "Running",
    "ValidatorAgent": "Running",
}

def print_execution_tree():
    """Print live execution tree"""
    print("\n EXECUTION TREE:")
    print("-" * 40)
    print(f"User Query")
    print(f"    ↓")
    print(f"Orchestrator          {execution_tree['Orchestrator']}")
    print(f"    ↓")
    print(f"    ├── Worker1       {execution_tree['Worker1']}")
    print(f"    ├── Worker2       {execution_tree['Worker2']}  ← Parallel")
    print(f"    └── Worker3       {execution_tree['Worker3']}")
    print(f"    ↓")
    print(f"Reflection Agent      {execution_tree['ReflectionAgent']}")
    print(f"    ↓")
    print(f"Validator Agent       {execution_tree['ValidatorAgent']}")
    print("-" * 40)

def run_worker(worker, task, worker_name):
    """Run a single worker on its task"""
    worker_proxy = autogen.UserProxyAgent(
        name=f"Proxy_{worker_name}",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    
    worker_proxy.initiate_chat(
        worker,
        message=task
    )
    
    # Store result
    messages = worker_proxy.chat_messages[worker]
    worker_results[worker_name] = messages[-1]['content']
    
    # Update execution tree
    execution_tree[worker_name] = "Done"
    print_execution_tree()

if __name__ == "__main__":
    print("-" * 60)
    print(" Starting Multi-Agent Pipeline - Day 2")
    print("Flow: User → Orchestrator → Workers(Parallel) → Reflection → Validator")
    print("-" * 60)

    # Step 1: Orchestrator creates tasks
    print("\n STEP 1: Orchestrator creating tasks...")
    print_execution_tree()
    
    orchestrator_proxy = autogen.UserProxyAgent(
        name="OrchestratorProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    
    user_query = "What is Artificial Intelligence and what are its applications?"
    
    orchestrator_proxy.initiate_chat(
        planner,
        message=user_query
    )
    
    # Update tree
    execution_tree["Orchestrator"] = "Done"
    print_execution_tree()

    # Step 2: Run all 3 workers in PARALLEL
    print("\n STEP 2: Running Workers in Parallel...")
    
    task1 = f"Based on this query: '{user_query}' - Research and explain what Artificial Intelligence is"
    task2 = f"Based on this query: '{user_query}' - Research and explain the applications of AI in healthcare and finance"
    task3 = f"Based on this query: '{user_query}' - Research and explain the applications of AI in transportation and customer service"
    
    # Create threads
    thread1 = threading.Thread(target=run_worker, args=(worker1, task1, "Worker1"))
    thread2 = threading.Thread(target=run_worker, args=(worker2, task2, "Worker2"))
    thread3 = threading.Thread(target=run_worker, args=(worker3, task3, "Worker3"))
    
    # Start all at the same time
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Wait for all to finish
    thread1.join()
    thread2.join()
    thread3.join()
    
    print("\n All workers completed in parallel!")

    # Step 3: Reflection Agent
    print("\n STEP 3: Reflection Agent improving answer...")
    
    combined_results = f"""
    Worker1 Result: {worker_results.get('Worker1', '')}
    Worker2 Result: {worker_results.get('Worker2', '')}
    Worker3 Result: {worker_results.get('Worker3', '')}
    
    Please combine and improve these results into one cohesive answer.
    """
    
    reflection_proxy = autogen.UserProxyAgent(
        name="ReflectionProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    
    reflection_proxy.initiate_chat(
        reflection_agent,
        message=combined_results
    )
    
    reflection_output = reflection_proxy.chat_messages[reflection_agent][-1]['content']
    
    # Update tree
    execution_tree["ReflectionAgent"] = "Done"
    print_execution_tree()

    # Step 4: Validator
    print("\n STEP 4: Validator checking answer...")
    
    validator_proxy = autogen.UserProxyAgent(
        name="ValidatorProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    
    validator_proxy.initiate_chat(
        validator,
        message=reflection_output
    )
    
    # Update tree
    execution_tree["ValidatorAgent"] = "Done"
    print_execution_tree()
    
    print("\n Pipeline Complete!")