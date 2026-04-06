# Quickstart: Payment CLI Simulator

## Prerequisites

- Python 3.11 or higher

## Installation

```bash
# Clone/navigate to repository root
cd claude-speckit-template

# No dependencies to install (stdlib only)
```

## Running the Application

```bash
python -m src.main
```

Or directly:

```bash
python src/main.py
```

## Basic Usage

### Process a Payment

```
> pay
Enter payment amount (USD): 50.00
Enter card number: 4111111111111111
Enter expiry date (MM/YY): 12/26
Enter CVV: 123

Processing payment...

✓ Payment Successful
Transaction ID: txn_a1b2c3d4-e5f6-7890-abcd-ef1234567890
Amount: $50.00
Card: ****-****-****-1111
```

### View Transaction History

```
> history
Transaction History
-------------------
1. txn_abc123... | $50.00 | ****1111 | SUCCESS | 2026-04-06 14:30:22

Total: 1 transaction
```

### Get Help

```
> help
Available commands:
  pay      - Process a new payment
  history  - View transaction history
  help     - Show this help message
  quit     - Exit the application
```

### Exit

```
> quit
Goodbye!
```

## Testing Failure Scenarios

### Test Declined Card

Use a card number ending in `0001`:

```
> pay
Enter payment amount (USD): 100
Enter card number: 4111111111110001
Enter expiry date (MM/YY): 12/26
Enter CVV: 123

Processing payment...

✗ Payment Failed
Reason: Card declined by issuer
```

### Test Insufficient Funds

Use amount `999.99`:

```
> pay
Enter payment amount (USD): 999.99
Enter card number: 4111111111111111
...

✗ Payment Failed
Reason: Insufficient funds
```

### Test Network Timeout

Use a card number ending in `0002`:

```
> pay
Enter payment amount (USD): 50
Enter card number: 4111111111110002
...

✗ Payment Failed
Reason: Network timeout - please try again
```

## Test Card Numbers

For successful payments, use any card number that:
- Is 13-19 digits
- Passes Luhn algorithm

Common test numbers (Luhn-valid):
- `4111111111111111` (Visa-like)
- `5500000000000004` (Mastercard-like)
- `340000000000009` (Amex-like)

## Running Tests

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=src
```
