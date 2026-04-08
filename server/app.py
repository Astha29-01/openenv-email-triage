from fastapi import FastAPI
from pydantic import BaseModel
from env import EmailTriageEnv

app = FastAPI(title="OpenEnv Email Triage")

env_instance = EmailTriageEnv()


class ResetRequest(BaseModel):
    task_id: str = "easy_spam_cleanup"


@app.get("/")
def home():
    return {"message": "OpenEnv Email Triage is running"}


@app.post("/reset")
def reset(req: ResetRequest):
    obs = env_instance.reset(req.task_id)
    return obs.dict()


@app.post("/step")
def step(action: dict):
    from models import Action
    action_obj = Action(**action)
    result = env_instance.step(action_obj)
    return result.dict()