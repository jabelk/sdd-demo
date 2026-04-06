"""Card model for payment validation."""

from dataclasses import dataclass


@dataclass
class Card:
    """Represents payment card information for validation.

    This is a transient validation object - card data is never stored
    or persisted after validation.

    Attributes:
        number: Full card number (13-19 digits)
        expiry_month: Expiration month (1-12)
        expiry_year: Expiration year (2-digit, e.g., 26 for 2026)
        cvv: Card verification value (3-4 digits)
    """
    number: str
    expiry_month: int
    expiry_year: int
    cvv: str

    def get_last_four(self) -> str:
        """Return the last 4 digits of the card number."""
        digits = "".join(c for c in self.number if c.isdigit())
        return digits[-4:] if len(digits) >= 4 else digits
