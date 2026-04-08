from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field


class EmailItem(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    received_at: str


class Observation(BaseModel):
    task_id: str
    task_description: str
    inbox: List[EmailItem]
    archived: List[str] = Field(default_factory=list)
    escalated: List[str] = Field(default_factory=list)
    drafts: Dict[str, str] = Field(default_factory=dict)
    classifications: Dict[str, str] = Field(default_factory=dict)
    priorities: Dict[str, str] = Field(default_factory=dict)
    step_count: int
    max_steps: int


class Action(BaseModel):
    action_type: Literal[
        "classify_email",
        "archive_email",
        "draft_reply",
        "send_reply",
        "escalate_email",
        "mark_priority",
        "noop"
    ]
    email_id: Optional[str] = None
    label: Optional[str] = None
    reply_text: Optional[str] = None
    priority: Optional[str] = None


class Reward(BaseModel):
    value: float
    reason: str


class StepResult(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict