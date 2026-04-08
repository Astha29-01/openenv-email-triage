from copy import deepcopy
from models import EmailItem, Observation, Reward, StepResult
from tasks import TASKS
from graders import grade_task


class EmailTriageEnv:
    def __init__(self):
        self.current_task = None
        self.state_data = {}

    def reset(self, task_id: str = "easy_spam_cleanup"):
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id: {task_id}")

        task = deepcopy(TASKS[task_id])
        self.current_task = task

        self.state_data = {
            "task_id": task["task_id"],
            "task_description": task["description"],
            "inbox": [EmailItem(**e) for e in task["emails"]],
            "archived": [],
            "escalated": [],
            "drafts": {},
            "classifications": {},
            "priorities": {},
            "step_count": 0,
            "max_steps": task["max_steps"]
        }

        return self._get_observation()

    def _get_observation(self):
        return Observation(
            task_id=self.state_data["task_id"],
            task_description=self.state_data["task_description"],
            inbox=self.state_data["inbox"],
            archived=self.state_data["archived"],
            escalated=self.state_data["escalated"],
            drafts=self.state_data["drafts"],
            classifications=self.state_data["classifications"],
            priorities=self.state_data["priorities"],
            step_count=self.state_data["step_count"],
            max_steps=self.state_data["max_steps"]
        )

    def state(self):
        return {
            "task_id": self.state_data["task_id"],
            "task_description": self.state_data["task_description"],
            "inbox": [e.dict() for e in self.state_data["inbox"]],
            "archived": self.state_data["archived"],
            "escalated": self.state_data["escalated"],
            "drafts": self.state_data["drafts"],
            "classifications": self.state_data["classifications"],
            "priorities": self.state_data["priorities"],
            "step_count": self.state_data["step_count"],
            "max_steps": self.state_data["max_steps"]
        }

    def step(self, action):
        self.state_data["step_count"] += 1
        reward_value = 0.0
        reason = "No effect"

        email_ids = {e.id for e in self.state_data["inbox"]}

        if action.action_type != "noop" and action.email_id and action.email_id not in email_ids:
            reward_value = -0.2
            reason = "Invalid email_id"

        elif action.action_type == "classify_email" and action.email_id and action.label:
            self.state_data["classifications"][action.email_id] = action.label
            reward_value = 0.2
            reason = "Email classified"

        elif action.action_type == "mark_priority" and action.email_id and action.priority:
            self.state_data["priorities"][action.email_id] = action.priority
            reward_value = 0.2
            reason = "Priority marked"

        elif action.action_type == "archive_email" and action.email_id:
            if action.email_id not in self.state_data["archived"]:
                self.state_data["archived"].append(action.email_id)
                reward_value = 0.3
                reason = "Email archived"

        elif action.action_type == "draft_reply" and action.email_id and action.reply_text:
            self.state_data["drafts"][action.email_id] = action.reply_text
            reward_value = 0.3
            reason = "Reply drafted"

        elif action.action_type == "send_reply" and action.email_id:
            if action.email_id in self.state_data["drafts"]:
                reward_value = 0.2
                reason = "Reply sent"

        elif action.action_type == "escalate_email" and action.email_id:
            if action.email_id not in self.state_data["escalated"]:
                self.state_data["escalated"].append(action.email_id)
                reward_value = 0.3
                reason = "Email escalated"

        elif action.action_type == "noop":
            reward_value = -0.05
            reason = "No operation"

        done = self.state_data["step_count"] >= self.state_data["max_steps"]

        if done:
            final_score = grade_task(
                self.current_task["task_id"],
                self.state(),
                self.current_task["expected"]
            )
            reward_value += final_score
            reason += f" | Final task score: {final_score}"

        return StepResult(
            observation=self._get_observation(),
            reward=Reward(value=round(reward_value, 2), reason=reason),
            done=done,
            info={"task_id": self.current_task["task_id"]}
        )