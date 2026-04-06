# Research: Payment CLI Simulator

**Feature**: 001-payment-cli-simulator
**Date**: 2026-04-06

## Technology Decisions

### 1. Programming Language

**Decision**: Python 3.11+

**Rationale**:
- Excellent stdlib support for CLI applications (argparse not needed for interactive mode)
- Built-in `input()` for interactive prompts
- Cross-platform compatibility out of the box
- Simple deployment (single script or package)
- `uuid` module for transaction IDs
- `datetime` for timestamp handling
- `time.sleep()` for processing delay simulation

**Alternatives Considered**:
- Node.js: Would require npm setup, more complex for simple CLI
- Go: Compiled binary is nice, but overkill for simulation tool
- Bash: Limited data structures, harder to test

### 2. Dependencies

**Decision**: Standard library only (no external packages)

**Rationale**:
- Spec describes a "simple CLI app"
- No complex terminal UI requirements (no need for rich, click, prompt_toolkit)
- Built-in `input()` sufficient for interactive prompts
- Keeps installation simple (`python main.py`)
- Reduces maintenance burden

**Alternatives Considered**:
- `click`: Nice CLI framework but adds dependency for simple prompts
- `rich`: Beautiful output but unnecessary for this scope
- `prompt_toolkit`: Advanced input handling not required

### 3. Luhn Algorithm Implementation

**Decision**: Custom implementation (stdlib only)

**Rationale**:
- Algorithm is simple (10-15 lines of code)
- Avoids external dependency for single function
- Well-documented algorithm, easy to test
- No edge cases that would benefit from battle-tested library

**Implementation approach**:
```python
def luhn_check(card_number: str) -> bool:
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0
```

### 4. Transaction ID Generation

**Decision**: UUID4 (stdlib `uuid` module)

**Rationale**:
- Guaranteed uniqueness per FR-006
- Industry standard format
- No collision concerns for session-based usage
- Human-readable when truncated for display

**Format**: Full UUID4 string (e.g., `txn_a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

### 5. Card Masking Strategy

**Decision**: Show only last 4 digits with asterisks

**Rationale**:
- Industry standard (PCI-DSS inspired, though simulation)
- Meets FR-012 and SC-005 requirements
- Format: `****-****-****-1234`

### 6. Failure Simulation Triggers

**Decision**: Magic values approach

**Rationale**:
- Simple to implement and document
- Predictable for testing
- Common pattern in payment sandbox environments (Stripe test cards)

**Trigger mapping**:
| Trigger | Condition | Response |
|---------|-----------|----------|
| Declined | Card ending in `0001` | "Card declined by issuer" |
| Insufficient funds | Amount = `999.99` | "Insufficient funds" |
| Network timeout | Card ending in `0002` | Simulated 5s delay + timeout error |

### 7. Interactive Loop Design

**Decision**: Command-based menu with prompts

**Rationale**:
- Matches FR-001 (interactive prompts) and FR-009 (history command)
- Clear separation between commands
- Easy to extend with new commands

**Commands**:
- `pay` - Start payment flow (prompts for details)
- `history` - Show transaction history
- `help` - Display available commands
- `quit` / `exit` - End session

## Best Practices Applied

### Input Validation

- Validate each field immediately after input (fail fast)
- Provide specific error messages per validation rule
- Allow retry without restarting entire flow
- Strip whitespace from inputs automatically

### Error Handling

- Catch `KeyboardInterrupt` (Ctrl+C) gracefully
- Never display raw exceptions to user
- Provide actionable error messages

### Testing Strategy

- Unit tests for validation functions (edge cases)
- Unit tests for processor logic (triggers, delays)
- Integration tests for full payment flows
- Use mocking for `time.sleep()` in tests to speed up

## Unresolved Items

None. All technical decisions made with stdlib-only constraint.
