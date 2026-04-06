"""Main entry point for the Payment CLI Simulator."""

import sys

from src.models.card import Card
from src.models.transaction import Transaction
from src.services.processor import process_payment
from src.services.history import TransactionHistory
from src.cli.prompts import prompt_amount, prompt_card_number, prompt_expiry, prompt_cvv
from src.cli.display import (
    mask_card_number,
    display_processing,
    display_success,
    display_error,
    display_history,
    display_help,
)


# Global transaction history for the session
history = TransactionHistory()


def handle_pay() -> None:
    """Handle the pay command - process a payment."""
    try:
        # Get payment amount
        amount = prompt_amount()
        if amount is None:
            print("\nPayment cancelled.")
            return

        # Get card number
        card_number = prompt_card_number()
        if card_number is None:
            print("\nPayment cancelled.")
            return

        # Get expiry date
        expiry = prompt_expiry()
        if expiry is None:
            print("\nPayment cancelled.")
            return

        # Get CVV
        cvv = prompt_cvv()
        if cvv is None:
            print("\nPayment cancelled.")
            return

        # Create card object
        card = Card(
            number=card_number,
            expiry_month=expiry[0],
            expiry_year=expiry[1],
            cvv=cvv
        )

        # Show processing message
        display_processing()

        # Process the payment
        response = process_payment(card, amount)

        # Create masked card for display
        masked_card = mask_card_number(card_number)

        # Record transaction in history
        transaction = Transaction.from_response(response, amount, masked_card)
        history.add(transaction)

        # Display result
        if response.success:
            display_success(response, amount, masked_card)
        else:
            display_error(response)

    except KeyboardInterrupt:
        print("\nPayment cancelled.")


def handle_history() -> None:
    """Handle the history command - show transaction history."""
    display_history(history.list())


def handle_help() -> None:
    """Handle the help command - show available commands."""
    display_help()


def main() -> None:
    """Main CLI loop."""
    print("Payment CLI Simulator")
    print("=" * 21)
    print("Type 'help' for available commands.")

    while True:
        try:
            command = input("\n> ").strip().lower()

            if not command:
                continue

            if command in ("quit", "exit"):
                print("Goodbye!")
                sys.exit(0)

            elif command == "pay":
                handle_pay()

            elif command == "history":
                handle_history()

            elif command in ("help", "?"):
                handle_help()

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nOperation cancelled. Type 'quit' to exit.")

        except EOFError:
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
