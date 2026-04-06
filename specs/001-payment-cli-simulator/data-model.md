# Data Model: Payment CLI Simulator

**Feature**: 001-payment-cli-simulator
**Date**: 2026-04-06

## Entities

### Transaction

Represents a payment attempt and its outcome.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `transaction_id` | string | Unique identifier | UUID4 format, prefixed with `txn_` |
| `amount` | decimal | Payment amount in USD | 0.01 ≤ amount ≤ 10000.00, 2 decimal places |
| `masked_card` | string | Last 4 digits of card | Format: `****-****-****-NNNN` |
| `status` | enum | Transaction outcome | `success` \| `failed` |
| `failure_reason` | string \| null | Reason for failure | Null if status is success |
| `response_code` | string | Processor response code | e.g., `APPROVED`, `DECLINED`, `INSUFFICIENT_FUNDS` |
| `timestamp` | datetime | When transaction occurred | ISO 8601 format |

**Lifecycle**:
```
[Created] → [Processing] → [Success | Failed]
```

Transactions are immutable after creation. No updates or deletes.

### Card (Validation Object)

Temporary object for input validation. Never stored or persisted.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `number` | string | Full card number | 13-19 digits, must pass Luhn check |
| `expiry_month` | int | Expiration month | 1-12 |
| `expiry_year` | int | Expiration year | 2-digit (YY), >= current year |
| `cvv` | string | Security code | 3-4 digits |

**Validation Rules**:
1. Card number: Numeric only, 13-19 characters, passes Luhn algorithm
2. Expiry: Not in the past (month/year >= current month/year)
3. CVV: 3 digits (Visa/MC/Discover) or 4 digits (Amex)

### PaymentResponse

Response returned to user after payment attempt.

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether payment succeeded |
| `transaction_id` | string | Unique transaction reference |
| `message` | string | Human-readable result message |
| `response_code` | string | Machine-readable status code |

**Response Codes**:
| Code | Description |
|------|-------------|
| `APPROVED` | Payment successful |
| `DECLINED` | Card declined by issuer |
| `INSUFFICIENT_FUNDS` | Not enough balance |
| `TIMEOUT` | Network/processor timeout |
| `INVALID_CARD` | Card validation failed |
| `EXPIRED_CARD` | Card expiry date in past |
| `INVALID_CVV` | CVV format invalid |
| `INVALID_AMOUNT` | Amount out of range |

## Relationships

```
┌─────────────┐
│    Card     │ ──validates──▶ ┌─────────────────┐
│ (transient) │                │   Transaction   │
└─────────────┘                │  (persistent*)  │
                               └────────┬────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ PaymentResponse │
                               │   (returned)    │
                               └─────────────────┘

* Persistent within session only (in-memory)
```

## Session State

### TransactionHistory

In-memory collection of transactions for current session.

| Operation | Description |
|-----------|-------------|
| `add(transaction)` | Append new transaction |
| `list()` | Return all transactions (newest first) |
| `count()` | Return number of transactions |
| `clear()` | Reset history (implicit on exit) |

**Storage**: Python list, cleared when process exits. Not persisted to disk.

## Failure Triggers (Magic Values)

For testing/simulation purposes:

| Trigger Type | Input Condition | Resulting Response Code |
|--------------|-----------------|-------------------------|
| Declined | Card number ends with `0001` | `DECLINED` |
| Insufficient Funds | Amount exactly `999.99` | `INSUFFICIENT_FUNDS` |
| Timeout | Card number ends with `0002` | `TIMEOUT` |

All other valid inputs result in `APPROVED`.
