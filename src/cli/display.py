"""Display utilities for CLI output."""

from typing import List

from src.models.response import PaymentResponse
from src.models.transaction import Transaction


def mask_card_number(card_number: str) -> str:
    """Mask a card number, showing only the last 4 digits.

    Args:
        card_number: The full card number

    Returns:
        Masked card number in format ****-****-****-NNNN
    """
    # Extract only digits
    digits = "".join(c for c in card_number if c.isdigit())

    if len(digits) < 4:
        return "****-****-****-" + digits

    last_four = digits[-4:]
    return f"****-****-****-{last_four}"


def display_processing() -> None:
    """Display processing message."""
    print("\nProcessing payment...")


def display_success(response: PaymentResponse, amount: float, masked_card: str) -> None:
    """Display successful payment response.

    Args:
        response: The payment response
        amount: The payment amount
        masked_card: The masked card number
    """
    print(f"\n\u2713 Payment Successful")
    print(f"Transaction ID: {response.transaction_id}")
    print(f"Amount: ${amount:.2f}")
    print(f"Card: {masked_card}")


def display_error(response: PaymentResponse) -> None:
    """Display failed payment response.

    Args:
        response: The payment response
    """
    print(f"\n\u2717 Payment Failed")
    print(f"Transaction ID: {response.transaction_id}")
    print(f"Reason: {response.message}")
    print(f"Response Code: {response.response_code.value}")


def display_history(transactions: List[Transaction]) -> None:
    """Display transaction history.

    Args:
        transactions: List of transactions to display
    """
    if not transactions:
        print("\nNo transactions yet.")
        return

    print("\nTransaction History")
    print("-" * 19)

    for i, txn in enumerate(transactions, 1):
        # Truncate transaction ID for display
        short_id = txn.transaction_id[:12] + "..."
        status = "SUCCESS" if txn.is_successful() else "FAILED"
        timestamp = txn.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        print(f"{i}. {short_id} | ${txn.amount:.2f} | {txn.masked_card[-4:]} | {status} | {timestamp}")

        if not txn.is_successful() and txn.failure_reason:
            print(f"   Reason: {txn.failure_reason}")

    print(f"\nTotal: {len(transactions)} transaction{'s' if len(transactions) != 1 else ''}")


def display_help() -> None:
    """Display available commands."""
    print("\nAvailable commands:")
    print("  pay      - Process a new payment")
    print("  history  - View transaction history")
    print("  help     - Show this help message")
    print("  quit     - Exit the application")
