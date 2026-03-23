import os
import sys
import shutil
import datetime

sys.path.append(os.path.dirname(__file__))

from config import LOG_DIR, OUTPUTS_DIR, MAX_RETRIES, token_usage
from tools import log
from agents import (
    orchestrator,
    planner,
    researcher,
    coder,
    analyst,
    critic,
    optimizer,
    validator,
    reporter
)

# outputs folder management
def prepare_outputs_folder():
    if os.path.exists(OUTPUTS_DIR):
        shutil.rmtree(OUTPUTS_DIR)
    os.makedirs(OUTPUTS_DIR)
    log("SYSTEM", "outputs folder ready")

# confidence report
def print_confidence_report(confidence):
    print("-" * 60)
    print("CONFIDENCE REPORT")
    print("-" * 60)
    for agent, status in confidence.items():
        padded = agent.ljust(15)
        print(f"  {padded} : {status}")
    print("-" * 60)

# main pipeline
def run_nexus_ai(task):
    start_time = datetime.datetime.now()

    print("-" * 60)
    print("NEXUS AI - Autonomous Multi-Agent System")
    print("-" * 60)
    print(f"Task: {task}")
    print("-" * 60)

    log("SYSTEM", f"Task started: {task}")

    # prepare fresh outputs folder
    prepare_outputs_folder()

    # confidence tracking
    confidence = {}

    # step 1 - orchestrator
    orchestrator_decision = orchestrator(task)
    agents_needed = orchestrator_decision["agents_needed"]
    language = orchestrator_decision["language"]
    project_folder = orchestrator_decision.get("project_folder", "nexus_output")
    confidence["Orchestrator"] = f"Confident - {orchestrator_decision['task_summary'][:50]}"

    # step 2 - planner
    plan = planner(task, orchestrator_decision)
    if plan.get("steps"):
        structure_count = len(plan.get("project_structure", []))
        confidence["Planner"] = f"Confident - {len(plan['steps'])} steps, {structure_count} files planned"
    else:
        confidence["Planner"] = "Low - fallback plan used"

    # initialize all outputs
    research = None
    code_data = None
    analysis = None
    critic_review = None
    optimized = None
    validation = None

    # step 3 - researcher
    if "Researcher" in agents_needed:
        research = researcher(task, plan, language)
        if research and research.get("findings") != "No research results found":
            sources = len(research.get("sources", []))
            confidence["Researcher"] = f"Confident - {sources} sources found"
        else:
            confidence["Researcher"] = "Low - no results found"
    else:
        confidence["Researcher"] = "Skipped - not needed for this task"

    # step 4 - coder
    if "Coder" in agents_needed:
        code_data = coder(task, plan, language, project_folder, research)
        if code_data and code_data.get("verified"):
            files_count = len(code_data.get("files", []))
            confidence["Coder"] = f"Confident - {files_count} files generated"
        else:
            confidence["Coder"] = "Low - files not verified"
    else:
        confidence["Coder"] = "Skipped - not needed for this task"

    # step 5 - analyst
    if "Analyst" in agents_needed:
        analysis = analyst(task, plan, language, research, code_data)
        if analysis and analysis.get("insights"):
            confidence["Analyst"] = f"Confident - {len(analysis['insights'])} insights found"
        else:
            confidence["Analyst"] = "Low - no insights generated"
    else:
        confidence["Analyst"] = "Skipped - not needed for this task"

    # step 6 - critic
    critic_review = critic(task, plan, language, code_data, analysis, research)
    if critic_review:
        verdict = critic_review.get("verdict", "UNKNOWN")
        issues = len(critic_review.get("issues", []))
        confidence["Critic"] = f"Confident - verdict: {verdict}, {issues} issues found"
    else:
        confidence["Critic"] = "Low - review failed"

    # step 7 - optimizer + validator retry loop
    for attempt in range(MAX_RETRIES):
        optimized = optimizer(task, plan, language, critic_review, code_data, analysis)

        if "Validator" in agents_needed:
            validation = validator(task, language, optimized, critic_review)

            if validation["status"] == "APPROVED":
                files_count = len(optimized.get("files", []))
                confidence["Optimizer"] = f"Confident - {files_count} files optimized"
                confidence["Validator"] = f"Confident - APPROVED on attempt {attempt+1}"
                log("Validator", "Solution approved")
                break
            else:
                log("Validator", f"Rejected - attempt {attempt+1} - retrying...")
                critic_review["feedback"] += f"\nValidator feedback: {validation['feedback']}"

                if attempt == MAX_RETRIES - 1:
                    confidence["Optimizer"] = "Low - could not fully optimize"
                    confidence["Validator"] = f"Low - REJECTED after {MAX_RETRIES} attempts"
        else:
            files_count = len(optimized.get("files", []))
            confidence["Optimizer"] = f"Confident - {files_count} files optimized"
            confidence["Validator"] = "Skipped - not needed for this task"
            break

    # step 8 - reporter
    report = reporter(task, language, optimized, analysis, research)
    if report:
        confidence["Reporter"] = f"Confident - docs saved to {project_folder}/"
    else:
        confidence["Reporter"] = "Low - minimal documentation saved"

    # time taken
    end_time = datetime.datetime.now()
    time_taken = (end_time - start_time).seconds

    # print confidence report
    print_confidence_report(confidence)

    # summary
    print("NEXUS AI Complete")
    print("-" * 60)
    print(f"Time taken   : {time_taken} seconds")
    print(f"Total tokens : {token_usage['total_tokens']}")
    print(f"API calls    : {token_usage['api_calls']}")
    print("-" * 60)
    print("Output files:")
    output_project = os.path.join(OUTPUTS_DIR, project_folder)
    if os.path.exists(output_project):
        for f in os.listdir(output_project):
            print(f"  - outputs/{project_folder}/{f}")
    else:
        for f in os.listdir(OUTPUTS_DIR):
            print(f"  - outputs/{f}")
    print("-" * 60)

    log("SYSTEM", f"Complete | Time: {time_taken}s | Tokens: {token_usage['total_tokens']} | Calls: {token_usage['api_calls']}")

    return {
        "project_folder": project_folder,
        "language": language,
        "optimized": optimized,
        "confidence": confidence,
        "tokens_used": token_usage["total_tokens"],
        "api_calls": token_usage["api_calls"]
    }

# interactive mode
def interactive_mode(last_result):
    while True:
        print("-" * 60)
        print("What do you want to do next?")
        print("-" * 60)
        print("  1. Run a new task")
        print("  2. Add more features to current project")
        print("  3. Add unit tests to current project")
        print("  4. Exit")
        print("-" * 60)

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            # run new task
            task = input("Enter your new task: ").strip()
            if not task:
                print("No task provided!")
                continue
            last_result = run_nexus_ai(task)

        elif choice == "2":
            # improve current project
            if not last_result:
                print("No current project to improve!")
                continue
            feature = input("What feature do you want to add? ").strip()
            if not feature:
                print("No feature provided!")
                continue
            # build improvement task
            project_folder = last_result.get("project_folder", "")
            language = last_result.get("language", "")
            improvement_task = f"Add {feature} to the existing {project_folder} project written in {language}"
            last_result = run_nexus_ai(improvement_task)

        elif choice == "3":
            # add unit tests
            if not last_result:
                print("No current project to test!")
                continue
            project_folder = last_result.get("project_folder", "")
            language = last_result.get("language", "")
            test_task = f"Write unit tests for the {project_folder} project written in {language}"
            last_result = run_nexus_ai(test_task)

        elif choice == "4":
            print("-" * 60)
            print("Thank you for using NEXUS AI!")
            print("-" * 60)
            break

        else:
            print("Invalid choice! Please enter 1, 2, 3 or 4")

# entry point
if __name__ == "__main__":
    print("-" * 60)
    print("Welcome to NEXUS AI")
    print("-" * 60)
    task = input("Enter your task: ").strip()
    if not task:
        print("No task provided!")
    else:
        last_result = run_nexus_ai(task)
        interactive_mode(last_result)
