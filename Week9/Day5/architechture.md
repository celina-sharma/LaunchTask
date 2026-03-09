## explain how all agents connect and work together
# ARCHITECTURE.md — NEXUS AI System Architecture

## Overview
NEXUS AI is a sequential multi-agent pipeline where each agent's output becomes the next agent's input.

---

## System Architecture
```
User Input (Task)
        ↓
┌─────────────────┐
│   Orchestrator  │ → Breaks task into subtasks
└─────────────────┘
        ↓
┌─────────────────┐
│     Planner     │ → Creates detailed step-by-step plan
└─────────────────┘
        ↓
┌─────────────────┐
│   Researcher    │ → Gathers relevant information
└─────────────────┘
        ↓
┌─────────────────┐
│     Coder       │ → Writes code or technical solution
└─────────────────┘
        ↓
┌─────────────────┐
│    Analyst      │ → Analyzes all results
└─────────────────┘
        ↓
┌─────────────────┐
│     Critic      │ → Reviews and identifies improvements
└─────────────────┘
        ↓
┌─────────────────┐
│   Optimizer     │ → Improves based on critic feedback
└─────────────────┘
        ↓
┌─────────────────┐
│   Validator     │ → Validates final solution
└─────────────────┘
        ↓
┌─────────────────┐
│    Reporter     │ → Generates final report
└─────────────────┘
        ↓
Final Report (saved to logs/)
```

---

## Data Flow
```
Task
→ Orchestrator Plan
→ Detailed Plan
→ Research Results
→ Code/Technical Solution
→ Analysis
→ Critique
→ Optimized Solution
→ Validation
→ Final Report
```

---

## Components

### 1. LLM Backend
- **Model**: llama-3.3-70b-versatile
- **Provider**: Groq API
- **Speed**: ~1 second per agent

### 2. Logging System
- **File**: logs/nexus_ai.log
- **Format**: timestamp - level - [agent] message
- **Reports**: logs/report_YYYYMMDD_HHMMSS.txt

### 3. Failure Recovery
- **Retries**: 3 attempts per agent
- **Timeout**: 60 seconds per request
- **Fallback**: Returns error message and continues pipeline

---

## Agent Details

| Agent | Input | Output |
|---|---|---|
| Orchestrator | Task | High-level plan |
| Planner | Task + Orchestrator plan | Detailed steps |
| Researcher | Task + Plan | Research findings |
| Coder | Task + Research | Code/Solution |
| Analyst | Task + Research + Code | Key insights |
| Critic | Task + Analysis | Critique |
| Optimizer | Task + Analysis + Critique | Improved solution |
| Validator | Task + Optimized solution | VALID/INVALID |
| Reporter | All outputs | Final report |

---

## Capabilities Map

| Capability | Implementation |
|---|---|
| Multi-agent orchestration | 9 agents in sequential pipeline |
| Multi-step planning | Planner agent |
| Role switching | Each agent has specific role |
| Self-reflection | Critic agent reviews work |
| Self-improvement | Optimizer improves based on critique |
| Logs + Tracing | Python logging to nexus_ai.log |
| Failure recovery | Retry mechanism in call_llm() |

---

## Technology Stack

| Component | Technology |
|---|---|
| LLM | Groq (llama-3.3-70b-versatile) |
| Language | Python 3.12 |
| Logging | Python logging module |
| Config | Python config file |