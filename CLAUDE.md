# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the **Claude + Spec Kit Template** - a reusable scaffolding for spec-driven development (SDD) workflows using Claude Code with GitHub Spec Kit.

## Repository Structure

```
sdd-demo/
└── claude-speckit-template/   # The actual template (copy this to start a new project)
    ├── CLAUDE.md              # Agent instructions (has {{PLACEHOLDERS}} to fill in)
    ├── AGENTS.md              # Agent read order and workflow rules
    ├── .specify/              # Spec Kit configuration and memory
    │   ├── memory/            # Constitution, project tracker, lessons learned
    │   ├── templates/         # Spec/plan/task templates
    │   └── scripts/bash/      # Helper scripts
    └── .claude/commands/      # 9 speckit.* slash commands
```

## Using the Template

1. Copy `claude-speckit-template/` to a new project directory
2. Fill in placeholders in `CLAUDE.md` and `AGENTS.md`:
   - `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`
   - `{{LANGUAGE}}`, `{{PACKAGE_MANAGER}}`
   - `{{INSTALL_COMMAND}}`, `{{TEST_COMMAND}}`, `{{LINT_COMMAND}}`, `{{BUILD_COMMAND}}`, `{{DEV_COMMAND}}`
3. Run `/speckit.constitution` to define project principles
4. Start building with `/speckit.specify <feature description>`

## Spec Kit Workflow

```
/speckit.constitution  →  Set project principles (once)
/speckit.specify       →  Write feature spec
/speckit.clarify       →  Resolve ambiguities (optional)
/speckit.plan          →  Design implementation
/speckit.tasks         →  Break into ordered tasks
/speckit.analyze       →  Check consistency (optional)
/speckit.checklist     →  Validate requirements (optional)
/speckit.implement     →  Execute tasks
/speckit.taskstoissues →  Convert tasks to GitHub Issues
```

## Key Concepts

- **Constitution**: Non-negotiable project principles in `.specify/memory/constitution.md`
- **Specs**: Feature specifications live in `specs/<feature>/spec.md`
- **Plans**: Implementation designs in `specs/<feature>/plan.md`
- **Tasks**: Ordered task breakdowns in `specs/<feature>/tasks.md`
- **GitHub Issues**: Primary work tracker (not parallel markdown files)

## Prerequisites

- Claude Code CLI
- Git
- GitHub CLI (`gh`) for issue tracking and PR creation
- Spec Kit CLI (optional): `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
