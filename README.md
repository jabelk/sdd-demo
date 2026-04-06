# Payment CLI Simulator

A demo payment processing CLI built using **spec-driven development (SDD)** with [Claude Code](https://claude.ai/code) and [GitHub Spec Kit](https://github.com/github/spec-kit).

Created for the **Cisco DevNet Month of AI** video series.

## What is Spec-Driven Development?

Spec-driven development is a methodology where you write detailed specifications before writing code. This project demonstrates the full workflow:

1. **Constitution** - Define non-negotiable project principles
2. **Specification** - Write clear requirements and acceptance criteria
3. **Plan** - Design the implementation approach
4. **Tasks** - Break the plan into ordered, dependency-aware tasks
5. **Implementation** - Execute tasks with full context

All artifacts are in the `specs/001-payment-cli-simulator/` directory.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/jabelk/sdd-demo.git
cd sdd-demo

# Run the payment simulator
python -m src.main

# Run tests
python -m pytest
```

## Features

- Process credit card payments (simulated)
- Card validation using the Luhn algorithm
- Expiration date and CVV validation
- Transaction history per session
- Configurable approval/decline rates

## Project Structure

```
├── src/
│   ├── main.py              # CLI entry point
│   ├── cli/                  # User interface
│   ├── models/               # Data models
│   └── services/             # Business logic
├── tests/                    # Unit and integration tests
├── specs/                    # SDD artifacts
│   └── 001-payment-cli-simulator/
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       └── tasks.md          # Task breakdown
├── .specify/                 # Spec Kit configuration
└── .claude/commands/         # Speckit slash commands
```

## Spec Kit Slash Commands

This repo includes 9 slash commands for the SDD workflow:

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Define project principles |
| `/speckit.specify` | Create a feature specification |
| `/speckit.clarify` | Ask clarifying questions |
| `/speckit.plan` | Generate implementation plan |
| `/speckit.tasks` | Break plan into tasks |
| `/speckit.analyze` | Check consistency |
| `/speckit.checklist` | Validate requirements |
| `/speckit.implement` | Execute tasks |
| `/speckit.taskstoissues` | Convert to GitHub Issues |

## Resources

- [Claude Code](https://claude.ai/code)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Cisco DevNet](https://developer.cisco.com/)

## License

MIT
