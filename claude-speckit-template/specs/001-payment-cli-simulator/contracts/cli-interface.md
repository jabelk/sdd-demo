# CLI Interface Contract: Payment CLI Simulator

**Feature**: 001-payment-cli-simulator
**Date**: 2026-04-06

## Overview

This document defines the user-facing interface contract for the Payment CLI Simulator.

## Entry Point

```bash
python -m src.main
# or
python src/main.py
```

## Interactive Commands

### Main Menu

After startup, user sees:

```
Payment CLI Simulator
=====================
Type 'help' for available commands.

> _
```

### Command: `help`

**Input**: `help` or `?`

**Output**:
```
Available commands:
  pay      - Process a new payment
  history  - View transaction history
  help     - Show this help message
  quit     - Exit the application
```

### Command: `pay`

**Input**: `pay`

**Flow** (interactive prompts):

```
> pay

Enter payment amount (USD): _
```

On valid amount:
```
Enter card number: _
```

On valid card:
```
Enter expiry date (MM/YY): _
```

On valid expiry:
```
Enter CVV: _
```

On valid CVV:
```
Processing payment...
[1-2 second delay]

✓ Payment Successful
Transaction ID: txn_a1b2c3d4-e5f6-7890-abcd-ef1234567890
Amount: $50.00
Card: ****-****-****-1234
```

**Error Output Examples**:

Invalid amount:
```
Enter payment amount (USD): -50
✗ Invalid amount. Must be between $0.01 and $10,000.00
Enter payment amount (USD): _
```

Invalid card (Luhn failure):
```
Enter card number: 1234567890123456
✗ Invalid card number.
Enter card number: _
```

Expired card:
```
Enter expiry date (MM/YY): 01/20
✗ Card has expired.
Enter expiry date (MM/YY): _
```

Invalid CVV:
```
Enter CVV: 12
✗ Invalid CVV. Must be 3 or 4 digits.
Enter CVV: _
```

### Command: `history`

**Input**: `history`

**Output (with transactions)**:
```
Transaction History
-------------------
1. txn_abc123... | $50.00  | ****1234 | SUCCESS | 2026-04-06 14:30:22
2. txn_def456... | $25.50  | ****5678 | FAILED  | 2026-04-06 14:28:15
   Reason: Card declined by issuer

Total: 2 transactions
```

**Output (empty)**:
```
No transactions yet.
```

### Command: `quit` / `exit`

**Input**: `quit`, `exit`, or Ctrl+D

**Output**:
```
Goodbye!
```

Process exits with code 0.

## Interrupt Handling

**Ctrl+C during prompt**:
```
^C
Operation cancelled. Type 'quit' to exit.
> _
```

**Ctrl+C during processing**:
```
Processing payment...
^C
Payment cancelled.
> _
```

## Failure Simulation Responses

### Declined Card (ends in 0001)
```
Processing payment...

✗ Payment Failed
Transaction ID: txn_xyz789...
Reason: Card declined by issuer
Response Code: DECLINED
```

### Insufficient Funds (amount = 999.99)
```
Processing payment...

✗ Payment Failed
Transaction ID: txn_xyz789...
Reason: Insufficient funds
Response Code: INSUFFICIENT_FUNDS
```

### Network Timeout (ends in 0002)
```
Processing payment...
[5 second delay]

✗ Payment Failed
Transaction ID: txn_xyz789...
Reason: Network timeout - please try again
Response Code: TIMEOUT
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Normal exit (quit command) |
| 1 | Unexpected error |

## Input Validation Summary

| Field | Valid Format | Error Message |
|-------|--------------|---------------|
| Amount | `0.01` - `10000.00` | "Invalid amount. Must be between $0.01 and $10,000.00" |
| Card Number | 13-19 digits, passes Luhn | "Invalid card number." |
| Expiry | `MM/YY`, not expired | "Card has expired." or "Invalid expiry format. Use MM/YY." |
| CVV | 3-4 digits | "Invalid CVV. Must be 3 or 4 digits." |
