# OpenEnv Email Triage Assistant

A real-world OpenEnv environment for training and evaluating AI agents on **email triage and inbox management**.

## Why this environment?

Modern AI agents are increasingly expected to operate in business workflows such as:

- cleaning spam-heavy inboxes
- handling support requests
- prioritizing urgent customer messages
- drafting professional replies
- escalating critical issues

This environment simulates those tasks through a structured API and deterministic graders.

---

## Real-world task simulated

This environment models a realistic **email triage assistant**.

The agent interacts with an inbox and must take actions such as:

- classify an email
- archive low-value or spam messages
- mark priority
- draft a reply
- send a reply
- escalate urgent issues

---

## OpenEnv-style API

### Endpoints

- `POST /reset`
- `POST /step`
- `GET /state`
- `GET /tasks`

---

## Observation Space

The observation includes:

- `task_id`
- `task_description`
- `inbox`
- `archived`
- `escalated`
- `drafts`
- `classifications`
- `priorities`
- `step_count`
- `max_steps`

---

## Action Space

Supported actions:

- `classify_email`
- `archive_email`
- `draft_reply`
- `send_reply`
- `escalate_email`
- `mark_priority`
- `noop`

---

## Reward Design

The reward function provides **partial progress signals**, not just end-of-task success.

Examples:
- Classifying correctly gives reward
- Archiving spam gives reward
- Drafting replies gives reward
- Invalid actions are penalized
- `noop` is slightly penalized
- Final grader score is added at episode end

This creates a denser and more useful learning signal for agents.

---

## Tasks

### 1. easy_spam_cleanup
**Difficulty:** Easy  
Archive spam/promotional emails and keep the legitimate support email.

### 2. medium_support_inbox
**Difficulty:** Medium  
Classify support and billing emails, prioritize them, and draft useful replies.

### 3. hard_exec_inbox
**Difficulty:** Hard  
Handle an executive inbox by escalating urgent issues, archiving noise, prioritizing correctly, and drafting strong replies.

---

## Graders

Each task has a deterministic grader returning a score in **[0.0, 1.0]**.

Grading checks include:

- whether required emails were archived
- whether urgent emails were escalated
- whether classifications were correct
- whether priorities were set correctly
- whether draft replies contain expected keywords

---

## Local Run

### Install
```bash
pip install -r requirements.txt