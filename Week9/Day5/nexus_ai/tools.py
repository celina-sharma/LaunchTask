# tools.py - core tools and utilities
import os
import json
import logging
from groq import Groq
from serpapi import GoogleSearch
from dotenv import load_dotenv
from config import (
    GROQ_API_KEY, SERPAPI_KEY,
    PRIMARY_MODEL, FALLBACK_MODEL,
    LOG_DIR, LOG_FILE, OUTPUTS_DIR,
    MAX_RETRIES, token_usage
)

# load env
load_dotenv()

# logging setup
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# groq client
client = Groq(api_key=GROQ_API_KEY)

# log function
def log(agent, message):
    log_message = f"[{agent}] {message}"
    print(log_message)
    logging.info(log_message)

# groq call with fallback
def call_groq(prompt, agent_name, use_fallback=False):
    model = FALLBACK_MODEL if use_fallback else PRIMARY_MODEL
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2048,
        )
        # token tracking
        token_usage["prompt_tokens"]     += response.usage.prompt_tokens
        token_usage["completion_tokens"] += response.usage.completion_tokens
        token_usage["total_tokens"]      += response.usage.total_tokens
        token_usage["api_calls"]         += 1

        return response.choices[0].message.content.strip()

    except Exception as e:
        if not use_fallback:
            log(agent_name, f"Primary model failed: {e} - switching to fallback")
            return call_groq(prompt, agent_name, use_fallback=True)
        else:
            log(agent_name, f"Fallback also failed: {e}")
            return None

# strip markdown backticks
def strip_backticks(code):
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:])
    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]
    return code.strip()

# web search
def web_search(query, agent_name):
    # check API key
    if not SERPAPI_KEY:
        log(agent_name, "SERPAPI_KEY not set - skipping search")
        return "No results found"

    for attempt in range(MAX_RETRIES):
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": SERPAPI_KEY,
                "num": 5
            })
            results = search.get_dict()
            organic = results.get("organic_results", [])

            if not organic:
                return "No results found"

            findings = []
            for r in organic[:5]:
                findings.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "link": r.get("link", "")
                })

            log(agent_name, f"Search complete: {len(findings)} results found")
            return json.dumps(findings, indent=2)

        except Exception as e:
            log(agent_name, f"Search attempt {attempt+1} failed: {e}")

    # all attempts failed
    log(agent_name, "All search attempts failed")
    return "No results found"

# code execution - language aware
def execute_code(code, agent_name, language="Python", filename=None):
    # strip backticks first
    code = strip_backticks(code)

    # non-python → just confirm code exists
    if language.lower() not in ["python", "python3"]:
        log(agent_name, f"{language} code generated successfully")
        return {
            "status": "success",
            "output": f"{language} code generated successfully"
        }

    # skip syntax check for non-code files
    non_code_extensions = [".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".gitignore", ".env"]
    is_non_code = any(ext in filename.lower() for ext in non_code_extensions) if filename else False

    if is_non_code:
        log(agent_name, "Non-code file - skipping syntax check")
        return {
            "status": "success",
            "output": "Non-code file generated successfully"
        }

    # python -> syntax check only
    try:
        import ast
        ast.parse(code)
        log(agent_name, "Syntax check passed")
        return {
            "status": "success",
            "output": "Python syntax verified successfully"
        }
    except SyntaxError as e:
        log(agent_name, f"Syntax error found: {e}")
        return {
            "status": "error",
            "output": f"Syntax error: {e}"
        }

# save file
def save_file(filename, content, agent_name, subfolder=None):
    try:
        # create path with optional subfolder
        if subfolder:
            folder_path = os.path.join(OUTPUTS_DIR, subfolder)
        else:
            folder_path = OUTPUTS_DIR

        # create folder if not exists
        os.makedirs(folder_path, exist_ok=True)

        filepath = os.path.join(folder_path, filename)
        with open(filepath, "w") as f:
            f.write(content)
        log(agent_name, f"File saved: {filename}")
        return filepath
    except Exception as e:
        log(agent_name, f"File save failed: {e}")
        return None
