# Claude + Spec Kit Template

A reusable scaffolding for **spec-driven development (SDD)** workflows using [Claude Code](https://claude.ai/code) with [GitHub Spec Kit](https://github.com/github/spec-kit).

Created for the **Cisco DevNet Month of AI** video series.

## What is Spec-Driven Development?

Spec-driven development is a methodology where you write detailed specifications before writing code. With Claude Code and Spec Kit, you can:

1. Define project principles in a constitution
2. Write feature specifications with clear requirements
3. Generate implementation plans
4. Break plans into ordered, dependency-aware tasks
5. Implement with full context of design decisions

This approach reduces ambiguity, improves code quality, and creates a clear audit trail of why decisions were made.

## Getting Started

### Prerequisites

- [Claude Code CLI](https://claude.ai/code)
- Git
- [GitHub CLI](https://cli.github.com/) (`gh`) for issue tracking and PR creation

### Using the Template

1. Copy the `claude-speckit-template/` directory to your new project:
   ```bash
   cp -r claude-speckit-template/ my-new-project/
   cd my-new-project/
   ```

2. Fill in the placeholders in `CLAUDE.md` and `AGENTS.md`:
   - `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`
   - `{{LANGUAGE}}`, `{{PACKAGE_MANAGER}}`
   - `{{INSTALL_COMMAND}}`, `{{TEST_COMMAND}}`, `{{LINT_COMMAND}}`, `{{BUILD_COMMAND}}`, `{{DEV_COMMAND}}`

3. Initialize your project principles:
   ```
   /speckit.constitution
   ```

4. Start building features:
   ```
   /speckit.specify <feature description>
   ```

## Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Define project principles (run once) |
| `/speckit.specify` | Create a feature specification |
| `/speckit.clarify` | Ask clarifying questions about the spec |
| `/speckit.plan` | Generate an implementation plan |
| `/speckit.tasks` | Break plan into ordered tasks |
| `/speckit.analyze` | Check consistency across artifacts |
| `/speckit.checklist` | Validate requirements coverage |
| `/speckit.implement` | Execute the implementation tasks |
| `/speckit.taskstoissues` | Convert tasks to GitHub Issues |

## Workflow Diagram

```
/speckit.constitution     (once per project)
        |
        v
/speckit.specify  ------>  specs/<feature>/spec.md
        |
        v
/speckit.clarify          (optional - resolve ambiguities)
        |
        v
/speckit.plan    ------>  specs/<feature>/plan.md
        |                  specs/<feature>/research.md
        |                  specs/<feature>/data-model.md
        v
/speckit.tasks   ------>  specs/<feature>/tasks.md
        |
        v
/speckit.analyze          (optional - consistency check)
        |
        v
/speckit.implement -----> Code!
        |
        v
/speckit.taskstoissues -> GitHub Issues
```

## Project Structure

```
claude-speckit-template/
├── CLAUDE.md                    # Agent instructions (fill in placeholders)
├── AGENTS.md                    # Agent workflow rules
├── .claude/commands/            # The 9 speckit.* slash commands
├── .specify/
│   ├── memory/
│   │   ├── constitution.md      # Project principles
│   │   ├── project-tracker.md   # Project state overview
│   │   ├── complexity-budget.md # LOC/dependency thresholds
│   │   └── lessons-learned/     # Knowledge base
│   ├── templates/               # Spec/plan/task templates
│   └── scripts/bash/            # Helper scripts
└── specs/                       # Feature specifications live here
    └── 001-payment-cli-simulator/  # Example feature
```

## Example Feature

The template includes a complete example: a **Payment CLI Simulator**. This demonstrates the full SDD workflow with:

- Feature specification (`specs/001-payment-cli-simulator/spec.md`)
- Implementation plan (`plan.md`)
- Task breakdown (`tasks.md`)
- Working Python code (`src/`)
- Tests (`tests/`)

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Cisco DevNet](https://developer.cisco.com/)

## License

MIT
