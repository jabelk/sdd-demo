# Tasks: Payment CLI Simulator

**Input**: Design documents from `/specs/001-payment-cli-simulator/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: TDD approach - tests included per constitution default (write tests before implementation).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Python package structure

- [x] T001 Create project directory structure per plan.md: `src/`, `src/models/`, `src/services/`, `src/cli/`, `tests/`, `tests/unit/`, `tests/integration/`
- [x] T002 Create Python package `__init__.py` files in src/, src/models/, src/services/, src/cli/, tests/, tests/unit/, tests/integration/
- [x] T003 [P] Create pytest configuration in pyproject.toml or pytest.ini
- [x] T004 [P] Create tests/conftest.py with shared test fixtures

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core entities and validation logic that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational Components

- [x] T005 [P] Unit tests for Luhn algorithm validation in tests/unit/test_validator.py
- [x] T006 [P] Unit tests for expiry date validation in tests/unit/test_validator.py
- [x] T007 [P] Unit tests for CVV validation in tests/unit/test_validator.py
- [x] T008 [P] Unit tests for amount validation in tests/unit/test_validator.py

### Implementation of Foundational Components

- [x] T009 [P] Create Card model (validation object) in src/models/card.py with fields: number, expiry_month, expiry_year, cvv
- [x] T010 [P] Create PaymentResponse model in src/models/response.py with fields: success, transaction_id, message, response_code
- [x] T011 [P] Create Transaction model in src/models/transaction.py with fields: transaction_id, amount, masked_card, status, failure_reason, response_code, timestamp
- [x] T012 Implement validator service in src/services/validator.py with: luhn_check(), validate_expiry(), validate_cvv(), validate_amount()
- [x] T013 Implement card masking utility in src/cli/display.py: mask_card_number() showing only last 4 digits as `****-****-****-NNNN`

**Checkpoint**: Foundation ready - Validation logic complete, all tests pass. User story implementation can now begin.

---

## Phase 3: User Story 1 - Process a Payment (Priority: P1) 🎯 MVP

**Goal**: User can run CLI, enter payment details via prompts, and receive success/failure response with transaction ID

**Independent Test**: Run `python -m src.main`, type `pay`, enter valid card details, verify success response with transaction ID

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T014 [P] [US1] Unit test for payment processor service in tests/unit/test_processor.py: test successful payment flow
- [x] T015 [P] [US1] Unit test for transaction ID generation (UUID format) in tests/unit/test_processor.py
- [x] T016 [P] [US1] Integration test for full payment flow in tests/integration/test_payment_flow.py: valid input → success response

### Implementation for User Story 1

- [x] T017 [P] [US1] Implement payment processor service in src/services/processor.py: process_payment() with 1-2 second delay simulation
- [x] T018 [US1] Implement interactive prompts in src/cli/prompts.py: prompt_amount(), prompt_card_number(), prompt_expiry(), prompt_cvv()
- [x] T019 [US1] Implement output display functions in src/cli/display.py: display_success(), display_error(), display_processing()
- [x] T020 [US1] Implement main CLI loop in src/main.py with `pay` command handler
- [x] T021 [US1] Implement `help` command in src/main.py showing available commands
- [x] T022 [US1] Add Ctrl+C (KeyboardInterrupt) handling in src/main.py for graceful interruption

**Checkpoint**: User Story 1 complete - User can process a payment via CLI and receive success/failure response with transaction ID. `help` and `quit` commands work.

---

## Phase 4: User Story 2 - View Transaction History (Priority: P2)

**Goal**: User can view list of all transactions processed in current session

**Independent Test**: Process 2-3 payments, type `history`, verify all transactions displayed with IDs, amounts, status, timestamps

### Tests for User Story 2

- [x] T023 [P] [US2] Unit test for history service in tests/unit/test_history.py: add, list, count operations
- [x] T024 [P] [US2] Integration test for history display in tests/integration/test_payment_flow.py: multiple payments → history shows all

### Implementation for User Story 2

- [x] T025 [US2] Implement history service in src/services/history.py: TransactionHistory class with add(), list(), count() methods
- [x] T026 [US2] Integrate history service into processor in src/services/processor.py: add transaction to history after processing
- [x] T027 [US2] Implement history display in src/cli/display.py: display_history() showing formatted transaction list
- [x] T028 [US2] Add `history` command handler in src/main.py

**Checkpoint**: User Story 2 complete - User can view full transaction history. Empty history shows appropriate message.

---

## Phase 5: User Story 3 - Simulate Payment Failures (Priority: P3)

**Goal**: User can trigger specific failure scenarios using magic values (declined, insufficient funds, timeout)

**Independent Test**: Use card ending in `0001` → DECLINED response; Use amount `999.99` → INSUFFICIENT_FUNDS; Use card ending in `0002` → TIMEOUT

### Tests for User Story 3

- [x] T029 [P] [US3] Unit test for decline trigger in tests/unit/test_processor.py: card ending 0001 → DECLINED
- [x] T030 [P] [US3] Unit test for insufficient funds trigger in tests/unit/test_processor.py: amount 999.99 → INSUFFICIENT_FUNDS
- [x] T031 [P] [US3] Unit test for timeout trigger in tests/unit/test_processor.py: card ending 0002 → TIMEOUT with 5s delay

### Implementation for User Story 3

- [x] T032 [US3] Add failure trigger detection in src/services/processor.py: check_failure_triggers() for magic values
- [x] T033 [US3] Implement declined response handling in src/services/processor.py
- [x] T034 [US3] Implement insufficient funds response handling in src/services/processor.py
- [x] T035 [US3] Implement timeout simulation (5s delay) in src/services/processor.py
- [x] T036 [US3] Update display functions in src/cli/display.py to show failure reason and response code

**Checkpoint**: User Story 3 complete - All failure triggers work consistently: declined, insufficient funds, timeout.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T037 [P] Validate all quickstart.md examples work correctly
- [x] T038 [P] Verify CLI interface matches contracts/cli-interface.md exactly
- [x] T039 Run full test suite and ensure 100% of acceptance scenarios pass
- [x] T040 Code review for card number masking - ensure no full card numbers in any output (SC-005)

---

## Implementation Complete

**All 40 tasks completed** - 47 tests passing

### Summary

- Phase 1 (Setup): 4/4 tasks ✓
- Phase 2 (Foundational): 9/9 tasks ✓
- Phase 3 (US1 - Process Payment): 9/9 tasks ✓
- Phase 4 (US2 - Transaction History): 6/6 tasks ✓
- Phase 5 (US3 - Failure Simulation): 8/8 tasks ✓
- Phase 6 (Polish): 4/4 tasks ✓
