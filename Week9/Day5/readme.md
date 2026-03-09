## explain what the project is and how to run it
# NEXUS AI — Autonomous Multi-Agent System

## Overview
NEXUS AI is a fully autonomous multi-agent AI system built for Day 5 of the LaunchPad program. It uses 9 specialized agents working together to solve complex tasks.

## Project Structure
```
Day5/
├── nexus_ai/
│   ├── main.py        # All 9 agents + pipeline
│   └── config.py      # Configuration settings
├── logs/              # Log files + reports
├── README.md          # This file
├── ARCHITECTURE.md    # System architecture
└── FINAL-REPORT.md    # Final project report
```

## Agents
| Agent | Role |
|---|---|
| Orchestrator | Manages all agents and assigns tasks |
| Planner | Creates detailed multi-step plans |
| Researcher | Researches and gathers information |
| Coder | Writes code and technical solutions |
| Analyst | Analyzes results and finds insights |
| Critic | Reviews work and identifies improvements |
| Optimizer | Improves solutions based on feedback |
| Validator | Validates final solution |
| Reporter | Generates final report |

## Capabilities
- Multi-agent orchestration
- Tool use
- Multi-step planning
- Role switching
- Logs + Tracing
- Failure recovery
- Self-reflection (Critic agent)
- Self-improvement (Optimizer agent)

## Setup

### Requirements
```bash
pip install groq
```

### Configuration
Add your Groq API key in `nexus_ai/config.py`:
```python
GROQ_API_KEY = "your_api_key_here"
```

### Run
```bash
python nexus_ai/main.py
```

## Example Tasks
1. "Plan a startup in AI for healthcare"
2. "Generate backend architecture for scalable app"
3. "Analyze CSV & create business strategy"
4. "Design a RAG pipeline for 50k documents"

## Model
- **Groq** — llama-3.3-70b-versatile (fast, free, local-friendly)

## Logs
- All agent activity logged to `logs/nexus_ai.log`
- Final reports saved to `logs/report_*.txt`