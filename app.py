from fastapi import FastAPI
from env import EmailTriageEnv
from models import Action

app = FastAPI(title="OpenEnv Email Triage")

env = EmailTriageEnv()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "OpenEnv Email Triage is running"
    }


@app.post("/reset")
def reset(payload: dict = {}):
    task_id = payload.get("task_id", "easy_spam_cleanup")
    obs = env.reset(task_id)
    return obs.dict()


@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return result.dict()


@app.get("/state")
def state():
    return env.state()