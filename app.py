from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from env import EmailTriageEnv
from models import Action

app = FastAPI(title="OpenEnv Email Triage")

env_instance = EmailTriageEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy_spam_cleanup"


@app.get("/")
def root():
    return {"message": "OpenEnv Email Triage is running"}


@app.post("/reset")
def reset_env(req: Optional[ResetRequest] = None):
    task_id = "easy_spam_cleanup"
    if req and req.task_id:
        task_id = req.task_id
    obs = env_instance.reset(task_id)
    return obs.dict()


@app.post("/step")
def step_env(action: Action):
    result = env_instance.step(action)
    return result.dict()


@app.get("/state")
def get_state():
    return env_instance.state()