from fastapi import FastAPI
from env import EmailTriageEnv

app = FastAPI()

env = EmailTriageEnv()

@app.get("/")
def home():
    return {"message": "OpenEnv Email Triage Assistant is running"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict()
    }

@app.post("/step")
def step(action: dict):
    result = env.step(action)
    return {
        "observation": result["observation"].dict(),
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"]
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def tasks():
    return {
        "tasks": ["easy", "medium", "hard"]
    }