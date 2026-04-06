"""Validation service for payment inputs."""

from datetime import datetime


def luhn_check(card_number: str) -> bool:
    """Validate a card number using the Luhn algorithm.

    Args:
        card_number: The card number to validate (may contain spaces)

    Returns:
        True if the card number is valid, False otherwise
    """
    # Remove spaces and extract only digits
    digits = [c for c in card_number if c.isdigit()]

    # Card number must be 13-19 digits
    if len(digits) < 13 or len(digits) > 19:
        return False

    # Check for non-digit characters (excluding spaces which we already removed)
    if any(c not in "0123456789 " for c in card_number):
        return False

    # Luhn algorithm
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        d = int(digit)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d

    return checksum % 10 == 0


def validate_expiry(month: int, year: int) -> bool:
    """Validate that a card expiry date is not in the past.

    Args:
        month: Expiry month (1-12)
        year: Expiry year (2-digit, e.g., 26 for 2026)

    Returns:
        True if the expiry date is valid and not in the past
    """
    # Validate month range
    if month < 1 or month > 12:
        return False

    # Validate year is not negative
    if year < 0:
        return False

    # Convert 2-digit year to 4-digit
    # Assume years 00-99 map to 2000-2099
    full_year = 2000 + year if year < 100 else year

    now = datetime.now()

    # Card is valid through the end of the expiry month
    if full_year > now.year:
        return True
    if full_year == now.year and month >= now.month:
        return True

    return False


def validate_cvv(cvv: str) -> bool:
    """Validate a CVV (Card Verification Value).

    Args:
        cvv: The CVV to validate

    Returns:
        True if the CVV is valid (3-4 digits)
    """
    if not cvv:
        return False

    # Must be exactly 3 or 4 digits
    if len(cvv) not in (3, 4):
        return False

    # Must be all numeric
    return cvv.isdigit()


def validate_amount(amount: float) -> bool:
    """Validate a payment amount.

    Args:
        amount: The payment amount in USD

    Returns:
        True if the amount is valid ($0.01 to $10,000.00)
    """
    # Minimum: $0.01
    # Maximum: $10,000.00
    return 0.01 <= amount <= 10000.00
