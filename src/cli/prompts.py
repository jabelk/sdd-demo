"""Interactive prompts for CLI input."""

from typing import Optional, Tuple

from src.services.validator import luhn_check, validate_expiry, validate_cvv, validate_amount


def prompt_amount() -> Optional[float]:
    """Prompt user for payment amount with validation.

    Returns:
        Valid amount or None if user cancels
    """
    while True:
        try:
            raw = input("Enter payment amount (USD): ").strip()

            if not raw:
                print("\u2717 Amount is required.")
                continue

            # Try to parse as float
            try:
                amount = float(raw)
            except ValueError:
                print("\u2717 Invalid amount format. Please enter a number.")
                continue

            if not validate_amount(amount):
                print("\u2717 Invalid amount. Must be between $0.01 and $10,000.00")
                continue

            return amount

        except EOFError:
            return None


def prompt_card_number() -> Optional[str]:
    """Prompt user for card number with Luhn validation.

    Returns:
        Valid card number or None if user cancels
    """
    while True:
        try:
            raw = input("Enter card number: ").strip()

            if not raw:
                print("\u2717 Card number is required.")
                continue

            # Remove any spaces for validation
            card_number = raw.replace(" ", "")

            if not luhn_check(card_number):
                print("\u2717 Invalid card number.")
                continue

            return card_number

        except EOFError:
            return None


def prompt_expiry() -> Optional[Tuple[int, int]]:
    """Prompt user for card expiry date.

    Returns:
        Tuple of (month, year) or None if user cancels
    """
    while True:
        try:
            raw = input("Enter expiry date (MM/YY): ").strip()

            if not raw:
                print("\u2717 Expiry date is required.")
                continue

            # Parse MM/YY format
            parts = raw.split("/")
            if len(parts) != 2:
                print("\u2717 Invalid expiry format. Use MM/YY.")
                continue

            try:
                month = int(parts[0])
                year = int(parts[1])
            except ValueError:
                print("\u2717 Invalid expiry format. Use MM/YY.")
                continue

            if not validate_expiry(month, year):
                print("\u2717 Card has expired.")
                continue

            return (month, year)

        except EOFError:
            return None


def prompt_cvv() -> Optional[str]:
    """Prompt user for CVV.

    Returns:
        Valid CVV or None if user cancels
    """
    while True:
        try:
            raw = input("Enter CVV: ").strip()

            if not raw:
                print("\u2717 CVV is required.")
                continue

            if not validate_cvv(raw):
                print("\u2717 Invalid CVV. Must be 3 or 4 digits.")
                continue

            return raw

        except EOFError:
            return None
