def grade_easy(state, expected):
    score = 0.0
    archived = set(state["archived"])
    classifications = state["classifications"]

    for email_id in expected["archive"]:
        if email_id in archived:
            score += 0.3

    for email_id in expected["keep"]:
        if email_id not in archived:
            score += 0.2

    for email_id, label in expected["classify"].items():
        if classifications.get(email_id) == label:
            score += 0.1

    return round(min(score, 1.0), 2)


def grade_medium(state, expected):
    score = 0.0
    classifications = state["classifications"]
    priorities = state["priorities"]
    drafts = state["drafts"]

    for email_id, label in expected["classify"].items():
        if classifications.get(email_id) == label:
            score += 0.2

    for email_id, priority in expected["priority"].items():
        if priorities.get(email_id) == priority:
            score += 0.2

    for email_id, keywords in expected["reply_keywords"].items():
        reply = drafts.get(email_id, "").lower()
        if all(k.lower() in reply for k in keywords):
            score += 0.2

    return round(min(score, 1.0), 2)


def grade_hard(state, expected):
    score = 0.0
    archived = set(state["archived"])
    escalated = set(state["escalated"])
    priorities = state["priorities"]
    drafts = state["drafts"]

    for email_id in expected["escalate"]:
        if email_id in escalated:
            score += 0.25

    for email_id in expected["archive"]:
        if email_id in archived:
            score += 0.2

    for email_id, priority in expected["priority"].items():
        if priorities.get(email_id) == priority:
            score += 0.15

    for email_id, keywords in expected["reply_keywords"].items():
        reply = drafts.get(email_id, "").lower()
        if all(k.lower() in reply for k in keywords):
            score += 0.125

    return round(min(score, 1.0), 2)


def grade_task(task_id, state, expected):
    if task_id == "easy_spam_cleanup":
        return grade_easy(state, expected)
    if task_id == "medium_support_inbox":
        return grade_medium(state, expected)
    if task_id == "hard_exec_inbox":
        return grade_hard(state, expected)
    return 0.0