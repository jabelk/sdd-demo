# Payment CLI Simulator

A demo payment processing CLI built using **spec-driven development (SDD)** with Claude Code and GitHub Spec Kit.

Created for the **Cisco DevNet Month of AI** video series.

## Tech Stack

- Python 3.11+ (stdlib only - no external dependencies)
- In-memory session-based storage

## Common Commands

| Action | Command |
|--------|---------|
| Run the app | `python -m src.main` |
| Run tests | `python -m pytest` |
| Run specific test | `python -m pytest tests/unit/test_processor.py` |

## Project Structure

```
├── src/
│   ├── main.py              # CLI entry point
│   ├── cli/                  # User interface (prompts, display)
│   ├── models/               # Data models (Card, Transaction, Response)
│   └── services/             # Business logic (processor, validator, history)
├── tests/
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── specs/                    # Feature specifications
│   └── 001-payment-cli-simulator/
├── .specify/                 # Spec Kit configuration
│   ├── memory/               # Constitution, lessons learned
│   └── templates/            # Spec/plan/task templates
└── .claude/commands/         # Speckit slash commands
```

## Spec-Driven Development

This project demonstrates the SDD workflow:

1. `/speckit.constitution` - Define project principles
2. `/speckit.specify` - Write feature specification
3. `/speckit.plan` - Create implementation plan
4. `/speckit.tasks` - Break into ordered tasks
5. `/speckit.implement` - Execute the tasks

See `specs/001-payment-cli-simulator/` for the complete spec, plan, and tasks.

## Features

- Process credit card payments (simulated)
- Card validation (Luhn algorithm, expiration, CVV)
- Transaction history per session
- Configurable approval/decline rates
- Clean CLI interface
