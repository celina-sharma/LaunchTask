import os
import logging
import datetime
from config import LLM_CONFIG, GROQ_API_KEY, GROQ_MODEL, LOG_FILE, LOG_DIR, MAX_RETRIES

# LOGGING SETUP
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(agent, message):
    """Log agent activity"""
    log_message = f"[{agent}] {message}"
    print(log_message)
    logging.info(log_message)


from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt, retries=MAX_RETRIES):
    """Call Groq LLM with failure recovery"""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            log("SYSTEM", f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                return f"Error: Failed after {retries} attempts"
    return None


# AGENTS
def orchestrator(task):
    """Orchestrator - manages all agents and assigns tasks"""
    log("Orchestrator", f"Received task: {task}")
    prompt = f"""You are the Orchestrator of NEXUS AI system.
You received this task: {task}

Your job:
1. Understand the task
2. Break it into subtasks
3. Assign each subtask to the right agent

Available agents: Planner, Researcher, Coder, Analyst, Critic, Optimizer, Validator, Reporter

Return a clear plan of which agent should do what.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Orchestrator", f"Plan created: {result}")
    return result


def planner(task, orchestrator_plan):
    """Planner - creates detailed multi-step plan"""
    log("Planner", "Creating detailed plan...")
    prompt = f"""You are the Planner of NEXUS AI system.
Task: {task}
Orchestrator plan: {orchestrator_plan}

Your job:
Create a detailed step-by-step plan to solve this task.
Number each step clearly.
Keep it concise and actionable.
"""
    result = call_llm(prompt)
    log("Planner", f"Plan: {result}")
    return result


def researcher(task, plan):
    """Researcher - researches the topic"""
    log("Researcher", "Researching topic...")
    prompt = f"""You are the Researcher of NEXUS AI system.
Task: {task}
Plan: {plan}

Your job:
Research and gather relevant information about this task.
Provide key facts, insights and relevant knowledge.
Keep it concise and relevant.
"""
    result = call_llm(prompt)
    log("Researcher", f"Research: {result}")
    return result


def coder(task, research):
    """Coder - writes and executes code if needed"""
    log("Coder", "Writing code...")
    prompt = f"""You are the Coder of NEXUS AI system.
Task: {task}
Research: {research}

Your job:
If this task requires code, write clean Python code to solve it.
If no code is needed, explain why and provide a technical solution instead.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Coder", f"Code: {result}")
    return result


def analyst(task, research, code):
    """Analyst - analyzes results"""
    log("Analyst", "Analyzing results...")
    prompt = f"""You are the Analyst of NEXUS AI system.
Task: {task}
Research: {research}
Code/Solution: {code}

Your job:
Analyze all the information and provide key insights.
Identify patterns, strengths and weaknesses.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Analyst", f"Analysis: {result}")
    return result


def critic(task, analysis):
    """Critic - reviews and critiques the work"""
    log("Critic", "Reviewing work...")
    prompt = f"""You are the Critic of NEXUS AI system.
Task: {task}
Analysis: {analysis}

Your job:
Review the work done and identify:
1. What is good
2. What needs improvement
3. What is missing
Be constructive and specific.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Critic", f"Critique: {result}")
    return result


def optimizer(task, analysis, critique):
    """Optimizer - improves based on critic feedback"""
    log("Optimizer", "Optimizing solution...")
    prompt = f"""You are the Optimizer of NEXUS AI system.
Task: {task}
Analysis: {analysis}
Critique: {critique}

Your job:
Based on the critique, improve and optimize the solution.
Address all the issues raised by the Critic.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Optimizer", f"Optimized solution: {result}")
    return result


def validator(task, optimized_solution):
    """Validator - validates the final solution"""
    log("Validator", "Validating solution...")
    prompt = f"""You are the Validator of NEXUS AI system.
Task: {task}
Optimized solution: {optimized_solution}

Your job:
Validate if this solution:
1. Solves the original task
2. Is complete and correct
3. Is ready for production

Return: VALID or INVALID with reasons.
Keep it concise.
"""
    result = call_llm(prompt)
    log("Validator", f"Validation: {result}")
    return result


def reporter(task, plan, research, analysis, optimized_solution, validation):
    """Reporter - generates final report"""
    log("Reporter", "Generating final report...")
    prompt = f"""You are the Reporter of NEXUS AI system.
Task: {task}

Generate a clear final report with:
1. Task Summary
2. Plan
3. Key Research Findings
4. Analysis
5. Final Solution
6. Validation Status

Use this information:
Plan: {plan}
Research: {research}
Analysis: {analysis}
Solution: {optimized_solution}
Validation: {validation}

Keep it clear and professional.
"""
    result = call_llm(prompt)
    log("Reporter", f"Report generated")
    return result


# MAIN PIPELINE
def run_nexus_ai(task):
    """Run the full NEXUS AI pipeline"""
    print("\n" + "=" * 60)
    print("NEXUS AI - Autonomous Multi-Agent System")
    print("=" * 60)
    print(f"Task: {task}")
    print("=" * 60 + "\n")

    log("SYSTEM", f"Starting NEXUS AI for task: {task}")

    # Step 1: Orchestrator
    orchestrator_plan = orchestrator(task)

    # Step 2: Planner
    detailed_plan = planner(task, orchestrator_plan)

    # Step 3: Researcher
    research = researcher(task, detailed_plan)

    # Step 4: Coder
    code_solution = coder(task, research)

    # Step 5: Analyst
    analysis = analyst(task, research, code_solution)

    # Step 6: Critic
    critique = critic(task, analysis)

    # Step 7: Optimizer
    optimized = optimizer(task, analysis, critique)

    # Step 8: Validator
    validation = validator(task, optimized)

    # Step 9: Reporter
    final_report = reporter(task, detailed_plan, research, analysis, optimized, validation)

    # Save report
    report_path = f"logs/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, "w") as f:
        f.write(f"Task: {task}\n\n")
        f.write(final_report)

    print("\n" + "=" * 60)
    print("FINAL REPORT:")
    print("=" * 60)
    print(final_report)
    print("\n" + "=" * 60)
    print(f"Report saved to: {report_path}")
    print("=" * 60)

    log("SYSTEM", "NEXUS AI pipeline complete!")
    return final_report


if __name__ == "__main__":
    print("=" * 60)
    print("Welcome to NEXUS AI")
    print("=" * 60)
    
    task = input("Enter your task: ").strip()
    run_nexus_ai(task)