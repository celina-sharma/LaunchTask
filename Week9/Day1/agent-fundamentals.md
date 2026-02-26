# AGENT FUNDAMENTALS — Week 9, Day 1

## What is an AI Agent?
An AI agent is a system that perceives its environment, reasons using an LLM,
and takes actions autonomously. Unlike chatbots that only respond, agents
can plan, use tools, and make decisions.

## Agent vs Chatbot vs Pipeline
- **Chatbot**: Only responds to messages, no autonomy
- **Pipeline**: Fixed sequence of steps, no decision-making
- **Agent**: Perceives → Reasons → Acts in a loop

## Perception → Reasoning → Action Loop
1. **Perception**: Agent receives input (user message)
2. **Reasoning**: Phi-3 thinks about what to do next
3. **Action**: Agent passes message to next agent
4. This loop continues until final answer is delivered

## ReAct Pattern (Reason + Act)
- Agent first thinks about the problem
- Then acts on it by passing to next agent
- Then observes the result
- Repeats until task is complete

## Agents Built

### 1. Research Agent
- **Role**: Gather raw information only
- **Input**: User query
- **Output**: Bullet points of raw facts
- **Does NOT**: Summarize or give final answers

### 2. Summarizer Agent
- **Role**: Compress raw info into structured summary
- **Input**: Output from Research Agent
- **Output**: Clean summary under 200 words
- **Does NOT**: Add new info or give final answers

### 3. Answer Agent
- **Role**: Deliver final user-friendly answer
- **Input**: Output from Summarizer Agent
- **Output**: Complete and friendly final answer
- **Does NOT**: Research or re-summarize

## Key Concepts Implemented

### Message Passing
Agents communicate by passing structured messages
to each other through the group chat manager.

### Role Control
Each agent is strictly controlled by its system prompt
to only perform its designated task.

### Task Delegation
- Research Agent delegates to Summarizer Agent
- Summarizer Agent delegates to Answer Agent

### Role Isolation
Each agent has ONE job only. They do not overlap
responsibilities making the system predictable.

### System Prompts for Agents
System prompts define each agent's role strictly.
They contain rules the agent must follow.

## Test Conversation Flow
```
User → Research Agent → Raw Information
Research Agent → Summarizer Agent → Summary
Summarizer Agent → Answer Agent → Final Answer
```

## Tech Stack
- Framework: AutoGen
- Model: Phi-3 via Ollama
- Language: Python 3.12