import requests
import sys

BASE_URL = "https://astha2901-openenv-email-triage.hf.space"

def main():
    task_id = "easy_spam_cleanup"

    print(f"[START] task={task_id}", flush=True)

    try:
        # Reset environment
        reset_resp = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id}, timeout=30)
        reset_resp.raise_for_status()
        obs = reset_resp.json()

        # Find first email
        inbox = obs.get("inbox", [])
        if not inbox:
            print(f"[END] task={task_id} score=0.0 steps=0", flush=True)
            return

        first_email = inbox[0]
        email_id = first_email["id"]

        # Example action: classify first email as spam
        action = {
            "action_type": "classify_email",
            "email_id": email_id,
            "label": "spam"
        }

        step_resp = requests.post(f"{BASE_URL}/step", json=action, timeout=30)
        step_resp.raise_for_status()
        result = step_resp.json()

        reward = result.get("reward", {}).get("value", 0.0)
        done = result.get("done", False)

        print(f"[STEP] step=1 reward={reward}", flush=True)

        final_score = reward if done else reward
        print(f"[END] task={task_id} score={final_score} steps=1", flush=True)

    except Exception as e:
        print(f"[END] task={task_id} score=0.0 steps=0 error={str(e)}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()