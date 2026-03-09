# FLOW DIAGRAM — Week 9, Day 2

## Multi-Agent Orchestration (Planner → Workers → Validator)

## Flow Diagram
```
User Query
    ↓
Orchestrator/Planner
(Breaks query into 3 tasks)
    ↓
    ├── Worker1 (Task 1)
    ├── Worker2 (Task 2)  ← Parallel Execution
    └── Worker3 (Task 3)
    ↓
Reflection Agent
(Combines and improves all worker outputs)
    ↓
Validator Agent
(Checks for errors and approves/rejects)
    ↓
Final Answer
```

## Agents and Their Roles

### 1. Orchestrator/Planner
- **File**: /orchestrator/planner.py
- **Role**: Receives user query and breaks it into 3 tasks
- **Input**: User query
- **Output**: 3 clearly defined tasks
- **Does NOT**: Execute tasks itself

### 2. Worker Agents
- **File**: /agents/worker_agent.py
- **Role**: Execute tasks assigned by Orchestrator
- **Input**: Task assigned by Orchestrator
- **Output**: Detailed response for their task
- **Runs**: In parallel (all 3 at the same time)

### 3. Reflection Agent
- **File**: /agents/reflection_agent.py
- **Role**: Combines all worker outputs into one improved answer
- **Input**: Outputs from all 3 workers
- **Output**: Clean and refined combined answer
- **Does NOT**: Add new information

### 4. Validator Agent
- **File**: /agents/validator.py
- **Role**: Checks final answer for errors
- **Input**: Output from Reflection Agent
- **Output**: VALIDATED or REJECTED with reason
- **Does NOT**: Rewrite the answer

## Key Concepts

### Planner-Executor Architecture
- Orchestrator is the Planner
- Workers are the Executors
- Clear separation between planning and execution

### DAG Based Execution
- Tasks flow in a Directed Acyclic Graph
- Orchestrator → Workers → Reflection → Validator
- No circular dependencies

### Parallel Execution
- All 3 workers work on different tasks simultaneously
- Reduces overall time to complete the query
- Each worker is independent of others

### Task Graph Generation
- Orchestrator generates a task graph
- Each node in the graph is a task
- Workers execute each node independently

## Tech Stack
- Framework: AutoGen
- Model: Phi-3 via Ollama
- Language: Python 3.12