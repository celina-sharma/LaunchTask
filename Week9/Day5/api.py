# api.py - NEXUS AI FastAPI Layer
import os
import sys
import shutil
import zipfile
import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), "nexus_ai"))

from nexus_ai.main import run_nexus_ai
from nexus_ai.config import OUTPUTS_DIR, token_usage
import nexus_ai.config as nexus_config

# fastapi app
app = FastAPI(
    title="NEXUS AI API",
    description="Autonomous Multi-Agent System API",
    version="1.0.0"
)

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# task history storage
task_history = []

# request model
class TaskRequest(BaseModel):
    task: str

# welcome
@app.get("/")
def welcome():
    return {
        "name": "NEXUS AI",
        "version": "1.0.0",
        "description": "Autonomous Multi-Agent System",
        "status": "running"
    }

# health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "outputs_dir": os.path.exists(OUTPUTS_DIR)
    }

# run task
@app.post("/run-task")
def run_task(request: TaskRequest):
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")

    try:
        # run nexus ai pipeline
        result = run_nexus_ai(request.task)

        project_folder = result.get("project_folder", "nexus_output")

        # get generated files
        output_path = os.path.join(OUTPUTS_DIR, project_folder)
        files = []
        if os.path.exists(output_path):
            files = os.listdir(output_path)

        # save to history
        history_entry = {
            "task": request.task,
            "project_folder": project_folder,
            "language": result.get("language", ""),
            "files": files,
            "timestamp": datetime.datetime.now().isoformat(),
            "tokens_used": result.get("tokens_used", 0),
            "api_calls": result.get("api_calls", 0)
        }
        task_history.append(history_entry)

        return {
            "status": "success",
            "task": request.task,
            "project_folder": project_folder,
            "language": result.get("language", ""),
            "files_generated": files,
            "confidence": result.get("confidence", {}),
            "tokens_used": token_usage["total_tokens"],
            "api_calls": token_usage["api_calls"],
            "timestamp": history_entry["timestamp"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# list files in project
@app.get("/files/{project_folder}")
def list_files(project_folder: str):
    output_path = os.path.join(OUTPUTS_DIR, project_folder)

    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail=f"Project folder '{project_folder}' not found")

    files = []
    for filename in os.listdir(output_path):
        filepath = os.path.join(output_path, filename)
        files.append({
            "filename": filename,
            "size": os.path.getsize(filepath),
            "path": f"outputs/{project_folder}/{filename}"
        })

    return {
        "project_folder": project_folder,
        "files": files,
        "total": len(files)
    }

# get file content
@app.get("/file/{project_folder}/{filename}")
def get_file_content(project_folder: str, filename: str):
    filepath = os.path.join(OUTPUTS_DIR, project_folder, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    try:
        with open(filepath, "r") as f:
            content = f.read()
        return {
            "filename": filename,
            "project_folder": project_folder,
            "content": content,
            "size": os.path.getsize(filepath)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# download single file
@app.get("/download/{project_folder}/{filename}")
def download_file(project_folder: str, filename: str):
    filepath = os.path.join(OUTPUTS_DIR, project_folder, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/octet-stream"
    )

# download all files as zip
@app.get("/download-zip/{project_folder}")
def download_zip(project_folder: str):
    output_path = os.path.join(OUTPUTS_DIR, project_folder)

    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail=f"Project folder '{project_folder}' not found")

    # create zip file
    zip_path = os.path.join(OUTPUTS_DIR, f"{project_folder}.zip")
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(output_path):
                filepath = os.path.join(output_path, filename)
                zipf.write(filepath, arcname=filename)

        return FileResponse(
            path=zip_path,
            filename=f"{project_folder}.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get task history
@app.get("/history")
def get_history():
    return {
        "total_tasks": len(task_history),
        "history": task_history
    }

# delete task history entry
@app.delete("/history/{project_folder}")
def delete_history(project_folder: str):
    global task_history

    # remove from history list
    task_history = [t for t in task_history if t["project_folder"] != project_folder]

    # remove from outputs folder
    output_path = os.path.join(OUTPUTS_DIR, project_folder)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # remove zip if exists
    zip_path = os.path.join(OUTPUTS_DIR, f"{project_folder}.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    return {
        "status": "deleted",
        "project_folder": project_folder
    }

# token usage
@app.get("/token-usage")
def get_token_usage():
    return {
    "prompt_tokens": nexus_config.token_usage["prompt_tokens"],
    "completion_tokens": nexus_config.token_usage["completion_tokens"],
    "total_tokens": nexus_config.token_usage["total_tokens"],
    "api_calls": nexus_config.token_usage["api_calls"]
}

# entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="localhost",
        port=8000,
        reload=False
    )