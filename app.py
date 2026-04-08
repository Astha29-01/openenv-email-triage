from fastapi import FastAPI
from models import Action
from env import EmailTriageEnv
from tasks import TASKS

app = FastAPI(title="OpenEnv Email Triage Assistant")

env = EmailTriageEnv()


@app.get("/")
def root():
    return {"message": "OpenEnv Email Triage Assistant is running"}


@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "task_id": task["task_id"],
                "description": task["description"],
                "max_steps": task["max_steps"]
            }
            for task in TASKS.values()
        ]
    }


@app.post("/reset")
def reset(task_id: str = "easy_spam_cleanup"):
    obs = env.reset(task_id)
    return obs.dict()


@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return result.dict()


@app.get("/state")
def state():
    return env.state()