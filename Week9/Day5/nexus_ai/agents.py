# agents.py - NEXUS AI Agents
import json
from config import MAX_RETRIES
from tools import log, call_groq, web_search, execute_code, save_file, strip_backticks

# orchestrator agent
def orchestrator(task):
    log("Orchestrator", f"Received task: {task}")

    prompt = f"""You are the Orchestrator of NEXUS AI.

Task: {task}

Step 1 - Understand what this task needs:
Think about:
- Does it need research? (finding information, best practices)
- Does it need code? (writing, executing, debugging code)
- Does it need analysis? (analyzing data, comparing options)
- Does it need documentation only?

Step 2 - Select ONLY agents actually needed:
Available agents:
- Planner    : always needed
- Researcher : needed if task requires finding information
- Coder      : needed if task requires writing or executing code
- Analyst    : needed if task requires analysis
- Critic     : always needed
- Optimizer  : always needed
- Validator  : needed if task has verifiable output
- Reporter   : always needed

Step 3 - Decide language:
- If user mentions language -> use exactly that
- If no language mentioned -> decide best language for this specific task

Return ONLY this JSON format, nothing else:
{{
    "task_summary": "brief summary of what task needs",
    "language": "",
    "project_folder": "short_project_name_lowercase_with_underscores",
    "agents_needed": ["Planner", "Coder", "Critic", "Optimizer", "Validator", "Reporter"],
    "reason": "why these agents were selected"
}}"""

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Orchestrator")
        if not result:
            log("Orchestrator", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            decision = json.loads(result[start:end])
            log("Orchestrator", f"Task summary: {decision['task_summary']}")
            log("Orchestrator", f"Language: {decision['language']}")
            log("Orchestrator", f"Agents selected: {decision['agents_needed']}")
            return decision
        except Exception as e:
            log("Orchestrator", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Orchestrator", "All attempts failed - using fallback")
    return {
        "task_summary": "Could not classify task - running full pipeline",
        "language": "",
        "project_folder": "nexus_output",
        "agents_needed": [
            "Planner", "Researcher", "Coder",
            "Analyst", "Critic", "Optimizer",
            "Validator", "Reporter"
        ],
        "reason": "fallback - could not classify task"
    }

# planner agent
def planner(task, orchestrator_decision):
    log("Planner", "Creating execution plan...")

    prompt = f"""You are the Planner of NEXUS AI.

Task: {task}
Task Summary: {orchestrator_decision['task_summary']}
Language: {orchestrator_decision['language']}
Agents Available: {orchestrator_decision['agents_needed']}

Create a clear structured execution plan.
Define exactly what each agent should do for this specific task.
Be specific and actionable.
Also define the project structure - list ONLY essential files needed.
Maximum 5 files for simple tasks, maximum 7 for complex tasks.
Only include actual code files - NO README, NO requirements.txt, NO .gitignore
Those will be generated automatically.
Each file should have a clear single responsibility.

Return ONLY this JSON format, nothing else:
{{
    "steps": [
        {{
            "agent": "Coder",
            "action": "exactly what this agent should do"
        }}
    ],
    "project_structure": [
        {{
            "filename": "main_file.py",
            "purpose": "brief purpose of this file"
        }}
    ]
}}"""

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Planner")
        if not result:
            log("Planner", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            plan = json.loads(result[start:end])
            if not plan.get("steps"):
                log("Planner", f"Attempt {attempt+1} returned empty steps")
                continue
            log("Planner", f"Plan created with {len(plan['steps'])} steps")
            return plan
        except Exception as e:
            log("Planner", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Planner", "All attempts failed - using fallback plan")
    return {
        "steps": [
            {"agent": "Coder", "action": "complete the task"},
            {"agent": "Critic", "action": "review the solution"},
            {"agent": "Reporter", "action": "generate documentation"}
        ],
        "project_structure": [
            {"filename": "solution.py", "purpose": "main solution file"}
        ]
    }

# researcher agent
def researcher(task, plan, language):
    log("Researcher", "Starting web research...")

    prompt_queries = f"""You are the Researcher of NEXUS AI.

Task: {task}
Language: {language}
Plan: {json.dumps(plan, indent=2)}

Generate 3 specific search queries to research this task.
Return ONLY this JSON format, nothing else:
{{
    "queries": [
        "search query 1",
        "search query 2",
        "search query 3"
    ]
}}"""

    # get search queries
    queries = [task]
    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt_queries, "Researcher")
        if not result:
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            parsed = json.loads(result[start:end])
            if parsed.get("queries"):
                queries = parsed["queries"]
                break
        except Exception as e:
            log("Researcher", f"Query generation attempt {attempt+1} failed: {e}")

    # actually search the web
    all_findings = []
    for query in queries:
        log("Researcher", f"Searching: {query}")
        findings = web_search(query, "Researcher")
        if findings and findings != "No results found":
            all_findings.append({
                "query": query,
                "results": findings
            })

    if not all_findings:
        log("Researcher", "No search results found")
        return {
            "findings": "No research results found",
            "sources": [],
            "key_points": []
        }

    # summarize findings
    prompt_summary = f"""You are the Researcher of NEXUS AI.

Task: {task}
Raw search results: {json.dumps(all_findings, indent=2)}

Summarize the most relevant findings for this task.
Include sources where available.
Be specific and factual.

Return ONLY this JSON format, nothing else:
{{
    "findings": "detailed summary of research findings",
    "sources": ["source1", "source2"],
    "key_points": ["point1", "point2", "point3"]
}}"""

    for attempt in range(MAX_RETRIES):
        summary = call_groq(prompt_summary, "Researcher")
        if not summary:
            continue
        try:
            start = summary.find("{")
            end = summary.rfind("}") + 1
            research = json.loads(summary[start:end])
            log("Researcher", "Research complete")
            return research
        except Exception as e:
            log("Researcher", f"Summary attempt {attempt+1} failed: {e}")

    # fallback
    log("Researcher", "Could not parse summary - returning raw findings")
    return {
        "findings": str(all_findings),
        "sources": [],
        "key_points": []
    }

# coder agent
def coder(task, plan, language, project_folder, research=None):
    log("Coder", "Writing code...")

    research_context = json.dumps(research, indent=2) if research else "No research provided"
    project_structure = plan.get("project_structure", [{"filename": "solution.py", "purpose": "main solution"}])

    all_files = []

    # generate each file one by one
    for file_info in project_structure:
        filename = file_info["filename"]
        purpose = file_info["purpose"]

        log("Coder", f"Writing {filename}...")

        prompt = f"""You are the Coder of NEXUS AI.

Task: {task}
Language: {language}
File to write: {filename}
Purpose of this file: {purpose}
All files in project: {json.dumps(project_structure, indent=2)}
Research: {research_context}

Write complete, clean, working code for {filename}.
This file's purpose is: {purpose}
Include all necessary imports.
Add clear comments.
Handle edge cases.
Make sure this file works with other files in the project.

Return in EXACTLY this format, nothing else:

FILENAME: {filename}
DEPENDENCIES: dependency1, dependency2 or none
---CODE---
complete code here
---END---"""

        for attempt in range(MAX_RETRIES):
            result = call_groq(prompt, "Coder")
            if not result:
                log("Coder", f"Attempt {attempt+1} call_groq returned None")
                continue
            try:
                # extract filename
                filename_line = [l for l in result.split("\n") if l.startswith("FILENAME:")]
                if not filename_line:
                    log("Coder", f"Attempt {attempt+1} missing FILENAME")
                    continue
                actual_filename = filename_line[0].replace("FILENAME:", "").strip()

                # extract dependencies
                deps_line = [l for l in result.split("\n") if l.startswith("DEPENDENCIES:")]
                dependencies = []
                if deps_line:
                    deps = deps_line[0].replace("DEPENDENCIES:", "").strip()
                    if deps.lower() != "none":
                        dependencies = [d.strip() for d in deps.split(",")]

                # extract code
                if "---CODE---" not in result or "---END---" not in result:
                    log("Coder", f"Attempt {attempt+1} missing code markers")
                    continue
                code = result.split("---CODE---")[1].split("---END---")[0].strip()
                code = strip_backticks(code)

                if not code:
                    log("Coder", f"Attempt {attempt+1} empty code")
                    continue

                # syntax check
                log("Coder", f"Checking {actual_filename}...")
                execution = execute_code(code, "Coder", language, actual_filename)

                if execution and execution["status"] == "success":
                    log("Coder", f"{actual_filename} verified successfully")
                    # save file in project folder
                    save_file(actual_filename, code, "Coder", project_folder)
                    all_files.append({
                        "filename": actual_filename,
                        "code": code,
                        "dependencies": dependencies,
                        "verified": True
                    })
                    break
                else:
                    error = execution["output"] if execution else "Unknown error"
                    log("Coder", f"Check failed: {error} - retrying...")
                    prompt += f"\n\nPrevious attempt failed:\n{error}\nFix this."

            except Exception as e:
                log("Coder", f"Attempt {attempt+1} failed: {e}")
        else:
            # all attempts failed for this file
            log("Coder", f"Could not generate {filename} - skipping")

    if not all_files:
        log("Coder", "No files generated - returning fallback")
        return {
            "files": [],
            "all_dependencies": [],
            "verified": False,
            "project_folder": project_folder
        }

    # collect all dependencies
    all_deps = []
    for f in all_files:
        for dep in f.get("dependencies", []):
            if dep not in all_deps:
                all_deps.append(dep)

    log("Coder", f"All {len(all_files)} files generated successfully")
    return {
        "files": all_files,
        "all_dependencies": all_deps,
        "verified": True,
        "project_folder": project_folder
    }
    
# analyst agent
def analyst(task, plan, language, research=None, code_data=None):
    log("Analyst", "Analyzing results...")

    research_context = json.dumps(research, indent=2) if research else "No research provided"
    # extract files summary for analyst context
    if code_data and code_data.get("files"):
        files_summary = [
            {
                "filename": f["filename"],
                "verified": f.get("verified", False)
            }
            for f in code_data["files"]
        ]
        code_context = json.dumps(files_summary, indent=2)
    else:
        code_context = "No code provided"

    prompt = f"""You are the Analyst of NEXUS AI.

Task: {task}
Language: {language}
Plan: {json.dumps(plan, indent=2)}
Research: {research_context}
Code: {code_context}

Analyze all the information and provide:
- Key insights
- Performance considerations
- Potential improvements
- Any risks or limitations

Return ONLY this JSON format, nothing else:
{{
    "insights": ["insight1", "insight2"],
    "performance": "performance analysis",
    "improvements": ["improvement1", "improvement2"],
    "risks": ["risk1", "risk2"]
}}"""

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Analyst")
        if not result:
            log("Analyst", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            analysis = json.loads(result[start:end])
            log("Analyst", "Analysis complete")
            return analysis
        except Exception as e:
            log("Analyst", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Analyst", "All attempts failed - returning empty analysis")
    return {
        "insights": [],
        "performance": "Analysis failed",
        "improvements": [],
        "risks": []
    }

# critic agent
def critic(task, plan, language, code_data=None, analysis=None, research=None):
    log("Critic", "Reviewing work...")

    # extract files summary for critic context
    if code_data and code_data.get("files"):
        files_summary = [
            {
                "filename": f["filename"],
                "verified": f.get("verified", False)
            }
            for f in code_data["files"]
        ]
        code_context = json.dumps(files_summary, indent=2)
    else:
        code_context = "No code provided"
    analysis_context = json.dumps(analysis, indent=2) if analysis else "No analysis provided"
    research_context = json.dumps(research, indent=2) if research else "No research provided"

    prompt = f"""You are the Critic of NEXUS AI.

Task: {task}
Language: {language}
Plan: {json.dumps(plan, indent=2)}
Code: {code_context}
Analysis: {analysis_context}
Research: {research_context}

Review all the work done and check:

Checklist:
1. Does it solve the original task?
2. Is the code complete and working?
3. Are edge cases handled?
4. Is the solution well structured?
5. Are there any missing parts?

For each checklist item answer YES or NO.
If ANY item is NO -> verdict is NEEDS_IMPROVEMENT.
If ALL items are YES -> verdict is APPROVED.

Return ONLY this JSON format, nothing else:
{{
    "checklist": {{
        "solves_task": "YES or NO",
        "code_complete": "YES or NO",
        "edge_cases": "YES or NO",
        "well_structured": "YES or NO",
        "nothing_missing": "YES or NO"
    }},
    "verdict": "APPROVED or NEEDS_IMPROVEMENT",
    "issues": ["issue1", "issue2"],
    "files_with_issues": ["filename1.py", "filename2.py"],
    "feedback": "specific feedback for improvement"
}}"""

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Critic")
        if not result:
            log("Critic", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            review = json.loads(result[start:end])
            log("Critic", f"Verdict: {review['verdict']}")
            return review
        except Exception as e:
            log("Critic", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Critic", "All attempts failed - returning default review")
    return {
        "checklist": {},
        "verdict": "NEEDS_IMPROVEMENT",
        "issues": ["Could not review properly"],
        "feedback": "Critic failed to parse response"
    }

# optimizer agent
def optimizer(task, plan, language, critic_review, code_data=None, analysis=None):
    log("Optimizer", "Optimizing solution...")

    analysis_context = json.dumps(analysis, indent=2) if analysis else "No analysis provided"
    project_folder = code_data.get("project_folder", "nexus_output") if code_data else "nexus_output"
    files = code_data.get("files", []) if code_data else []
    files_with_issues = critic_review.get("files_with_issues", [])
    if files_with_issues:
        files_to_optimize = [f for f in files if f["filename"] in files_with_issues]
        files_to_skip = [f for f in files if f["filename"] not in files_with_issues]
        log("Optimizer", f"Optimizing {len(files_to_optimize)} files, skipping {len(files_to_skip)}")
    else:
        files_to_optimize = files
        files_to_skip = []
        log("Optimizer", "No specific files flagged - optimizing all")

    if not files:
        log("Optimizer", "No files to optimize - returning empty")
        return {
            "files": [],
            "all_dependencies": [],
            "verified": False,
            "project_folder": project_folder
        }

    improved_files = []

    # add skipped files as is
    for file_info in files_to_skip:
        improved_files.append({
            "filename": file_info["filename"],
            "improved_code": file_info["code"],
            "dependencies": file_info.get("dependencies", []),
            "changes_made": [],
            "verified": file_info.get("verified", False)
        })
        log("Optimizer", f"Skipping {file_info['filename']} - no issues")

    # improve only files with issues
    for file_info in files_to_optimize:
        filename = file_info["filename"]
        current_code = file_info["code"]

        log("Optimizer", f"Optimizing {filename}...")

        prompt = f"""You are the Optimizer of NEXUS AI.

Task: {task}
Language: {language}
File to optimize: {filename}
Current code:
{current_code}

Critic Feedback: {json.dumps(critic_review, indent=2)}
Analysis: {analysis_context}

Based on the critic feedback:
1. Fix all issues mentioned
2. Improve the code quality
3. Make sure all checklist items pass
Keep the same filename and language.

Return in EXACTLY this format, nothing else:

FILENAME: {filename}
DEPENDENCIES: dependency1, dependency2 or none
CHANGES: change1, change2 or none
---CODE---
complete improved code here
---END---"""

        for attempt in range(MAX_RETRIES):
            result = call_groq(prompt, "Optimizer")
            if not result:
                log("Optimizer", f"Attempt {attempt+1} call_groq returned None")
                continue
            try:
                # extract filename
                filename_line = [l for l in result.split("\n") if l.startswith("FILENAME:")]
                if not filename_line:
                    log("Optimizer", f"Attempt {attempt+1} missing FILENAME")
                    continue
                actual_filename = filename_line[0].replace("FILENAME:", "").strip()

                # extract dependencies
                deps_line = [l for l in result.split("\n") if l.startswith("DEPENDENCIES:")]
                dependencies = []
                if deps_line:
                    deps = deps_line[0].replace("DEPENDENCIES:", "").strip()
                    if deps.lower() != "none":
                        dependencies = [d.strip() for d in deps.split(",")]

                # extract changes
                changes_line = [l for l in result.split("\n") if l.startswith("CHANGES:")]
                changes = []
                if changes_line:
                    ch = changes_line[0].replace("CHANGES:", "").strip()
                    if ch.lower() != "none":
                        changes = [c.strip() for c in ch.split(",")]

                # extract code
                if "---CODE---" not in result or "---END---" not in result:
                    log("Optimizer", f"Attempt {attempt+1} missing code markers")
                    continue
                improved_code = result.split("---CODE---")[1].split("---END---")[0].strip()
                improved_code = strip_backticks(improved_code)

                if not improved_code:
                    log("Optimizer", f"Attempt {attempt+1} empty code")
                    continue

                # syntax check
                log("Optimizer", f"Checking {actual_filename}...")
                execution = execute_code(improved_code, "Optimizer", language, actual_filename)

                if execution and execution["status"] == "success":
                    log("Optimizer", f"{actual_filename} verified")
                    # save improved file
                    save_file(actual_filename, improved_code, "Optimizer", project_folder)
                    improved_files.append({
                        "filename": actual_filename,
                        "improved_code": improved_code,
                        "dependencies": dependencies,
                        "changes_made": changes,
                        "verified": True
                    })
                    break
                else:
                    error = execution["output"] if execution else "Unknown error"
                    log("Optimizer", f"Check failed: {error} - retrying...")
                    prompt += f"\n\nFailed with error:\n{error}\nFix this."

            except Exception as e:
                log("Optimizer", f"Attempt {attempt+1} failed: {e}")

        else:
            # if all attempts failed keep original file
            log("Optimizer", f"Could not optimize {filename} - keeping original")
            improved_files.append({
                "filename": filename,
                "improved_code": current_code,
                "dependencies": file_info.get("dependencies", []),
                "changes_made": [],
                "verified": file_info.get("verified", False)
            })

    # collect all dependencies
    all_deps = []
    for f in improved_files:
        for dep in f.get("dependencies", []):
            if dep not in all_deps:
                all_deps.append(dep)

    log("Optimizer", f"All {len(improved_files)} files optimized")
    return {
        "files": improved_files,
        "all_dependencies": all_deps,
        "verified": True,
        "project_folder": project_folder
    }

# validator agent
def validator(task, language, optimized, critic_review):
    log("Validator", "Validating solution...")

    # rule based checks first
    rule_failures = []

    if not optimized:
        rule_failures.append("No solution provided")
    elif not optimized.get("files"):
        rule_failures.append("No files in solution")
    elif not optimized.get("verified"):
        rule_failures.append("Files not verified")

    if rule_failures:
        log("Validator", f"Rule based check failed: {rule_failures}")
        return {
            "status": "REJECTED",
            "rule_failures": rule_failures,
            "checklist": {},
            "feedback": "Failed rule based validation"
        }

    # build files summary for context
    files_summary = []
    for f in optimized.get("files", []):
        files_summary.append({
            "filename": f["filename"],
            "verified": f.get("verified", False),
            "changes": f.get("changes_made", [])
        })

    # checklist based check
    prompt = f"""You are the Validator of NEXUS AI.

Task: {task}
Language: {language}
Files generated: {json.dumps(files_summary, indent=2)}
Dependencies: {optimized.get("all_dependencies", [])}
Critic Review: {json.dumps(critic_review, indent=2)}

Validate the final solution against this checklist:
1. Does it completely solve the original task?
2. Is the code syntactically correct?
3. Are all critic issues resolved?
4. Is the solution well structured?
5. Are dependencies clearly listed?

Answer YES or NO for each.
If ALL are YES -> APPROVED
If ANY is NO -> REJECTED

Return ONLY this JSON format, nothing else:
{{
    "checklist": {{
        "solves_task": "YES or NO",
        "syntax_correct": "YES or NO",
        "critic_issues_resolved": "YES or NO",
        "well_structured": "YES or NO",
        "dependencies_listed": "YES or NO"
    }},
    "status": "APPROVED or REJECTED",
    "feedback": "reason for decision"
}}"""

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Validator")
        if not result:
            log("Validator", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            validation = json.loads(result[start:end])
            log("Validator", f"Validation status: {validation['status']}")
            return validation
        except Exception as e:
            log("Validator", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Validator", "All attempts failed - returning rejected")
    return {
        "checklist": {},
        "status": "REJECTED",
        "feedback": "Validator failed to parse response"
    }
    
# reporter agent
def reporter(task, language, optimized, analysis=None, research=None):
    log("Reporter", "Generating documentation...")

    analysis_context = json.dumps(analysis, indent=2) if analysis else "No analysis provided"
    research_context = json.dumps(research, indent=2) if research else "No research provided"
    project_folder = optimized.get("project_folder", "nexus_output") if optimized else "nexus_output"

    # get all generated files and dependencies
    files = optimized.get("files", []) if optimized else []
    all_deps = optimized.get("all_dependencies", []) if optimized else []
    deps_str = "\n".join(all_deps) if all_deps else "# no external dependencies"

    # build files list for README
    files_list = "\n".join([f"├── {f['filename']}" for f in files])
    if not files_list:
        files_list = "├── solution.py"

    prompt = f"""You are the Reporter of NEXUS AI.

Task: {task}
Language: {language}
Project folder: {project_folder}
Files generated:
{files_list}
Dependencies: {all_deps}
Analysis: {analysis_context}
Research: {research_context}

Generate a professional README.md for this project.
This should be task focused like a real developer README.
Do NOT mention agents or NEXUS AI internals.

Include:
- Project title
- Overview
- Project structure (use the actual files listed above)
- Installation (pip install -r requirements.txt or npm install)
- How to run
- API endpoints (if applicable)
- Examples
- License: MIT

Return in EXACTLY this format, nothing else:

---README---
complete markdown content here
---END---"""

    # gitignore based on language
    gitignore_content = {
        "python": """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
.env
venv/
.venv
*.egg
*.egg-info/
dist/
build/
.eggs/
.pytest_cache/
.coverage
*.log
*.db
*.sqlite3
instance/
.DS_Store""",
        "javascript": """# Node
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
.env
.env.local
dist/
build/
.DS_Store
*.log""",
        "java": """# Java
*.class
*.jar
*.war
*.ear
target/
.gradle/
build/
.idea/
*.iml
.DS_Store
*.log""",
        "default": """# General
.env
*.log
.DS_Store
build/
dist/
__pycache__/
node_modules/"""
    }

    for attempt in range(MAX_RETRIES):
        result = call_groq(prompt, "Reporter")
        if not result:
            log("Reporter", f"Attempt {attempt+1} call_groq returned None")
            continue
        try:
            # extract README
            if "---README---" not in result or "---END---" not in result:
                log("Reporter", f"Attempt {attempt+1} missing markers")
                continue

            readme = result.split("---README---")[1].split("---END---")[0].strip()

            if not readme:
                log("Reporter", f"Attempt {attempt+1} empty documentation")
                continue

            # get gitignore based on language
            lang_key = language.lower() if language else "default"
            if lang_key not in gitignore_content:
                lang_key = "default"
            gitignore = gitignore_content[lang_key]

            # save all files in project folder
            save_file("README.md", readme, "Reporter", project_folder)
            save_file("requirements.txt", deps_str, "Reporter", project_folder)
            save_file(".gitignore", gitignore, "Reporter", project_folder)

            log("Reporter", "Documentation complete")
            return {
                "readme": readme,
                "requirements": deps_str,
                "gitignore": gitignore,
                "project_folder": project_folder
            }

        except Exception as e:
            log("Reporter", f"Attempt {attempt+1} failed: {e}")

    # fallback
    log("Reporter", "All attempts failed - saving minimal documentation")
    save_file("README.md", f"# {task}\n\nDocumentation could not be generated.", "Reporter", project_folder)
    save_file("requirements.txt", deps_str, "Reporter", project_folder)
    lang_key = language.lower() if language else "default"
    save_file(".gitignore", gitignore_content.get(lang_key, gitignore_content["default"]), "Reporter", project_folder)
    return None