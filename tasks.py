TASKS = {
    "easy_spam_cleanup": {
        "task_id": "easy_spam_cleanup",
        "description": "Archive spam and promotional emails while keeping important emails in the inbox.",
        "max_steps": 8,
        "emails": [
            {
                "id": "e1",
                "sender": "promo@shopmart.com",
                "subject": "Big Sale Today!",
                "body": "Get 70% off now.",
                "received_at": "2026-04-08T09:00:00"
            },
            {
                "id": "e2",
                "sender": "support@company.com",
                "subject": "Need help with my order",
                "body": "I have an issue with my recent order.",
                "received_at": "2026-04-08T09:10:00"
            },
            {
                "id": "e3",
                "sender": "lottery@fakeprize.com",
                "subject": "You won $10,000!",
                "body": "Click here to claim your reward.",
                "received_at": "2026-04-08T09:20:00"
            }
        ],
        "expected": {
            "archive": ["e1", "e3"],
            "keep": ["e2"],
            "classify": {
                "e1": "spam",
                "e2": "support",
                "e3": "spam"
            }
        }
    },
    "medium_support_inbox": {
        "task_id": "medium_support_inbox",
        "description": "Handle support and billing emails by classifying, prioritizing, and drafting helpful replies.",
        "max_steps": 10,
        "emails": [
            {
                "id": "e1",
                "sender": "customer1@mail.com",
                "subject": "Refund request",
                "body": "I want a refund for my purchase.",
                "received_at": "2026-04-08T10:00:00"
            },
            {
                "id": "e2",
                "sender": "customer2@mail.com",
                "subject": "Invoice needed urgently",
                "body": "Please send my invoice before 5 PM today.",
                "received_at": "2026-04-08T10:15:00"
            }
        ],
        "expected": {
            "classify": {
                "e1": "support",
                "e2": "billing"
            },
            "priority": {
                "e1": "medium",
                "e2": "high"
            },
            "reply_keywords": {
                "e1": ["refund", "assist"],
                "e2": ["invoice", "today"]
            }
        }
    },
    "hard_exec_inbox": {
        "task_id": "hard_exec_inbox",
        "description": "Manage a mixed executive inbox by escalating urgent items, archiving low-value emails, prioritizing correctly, and drafting useful replies.",
        "max_steps": 12,
        "emails": [
            {
                "id": "e1",
                "sender": "vipclient@enterprise.com",
                "subject": "Production issue - urgent",
                "body": "Our system is down. Need immediate help.",
                "received_at": "2026-04-08T11:00:00"
            },
            {
                "id": "e2",
                "sender": "newsletter@techdigest.com",
                "subject": "Weekly AI News",
                "body": "Top stories of the week.",
                "received_at": "2026-04-08T11:05:00"
            },
            {
                "id": "e3",
                "sender": "ops@company.com",
                "subject": "Schedule leadership sync",
                "body": "Can we schedule a leadership sync tomorrow?",
                "received_at": "2026-04-08T11:10:00"
            }
        ],
        "expected": {
            "escalate": ["e1"],
            "archive": ["e2"],
            "priority": {
                "e1": "high",
                "e3": "medium"
            },
            "reply_keywords": {
                "e1": ["urgent", "investigating"],
                "e3": ["schedule", "tomorrow"]
            }
        }
    }
}