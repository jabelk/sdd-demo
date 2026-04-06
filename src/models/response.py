"""PaymentResponse model for processor responses."""

from dataclasses import dataclass
from enum import Enum


class ResponseCode(Enum):
    """Machine-readable response codes for payment processing."""
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    TIMEOUT = "TIMEOUT"
    INVALID_CARD = "INVALID_CARD"
    EXPIRED_CARD = "EXPIRED_CARD"
    INVALID_CVV = "INVALID_CVV"
    INVALID_AMOUNT = "INVALID_AMOUNT"


@dataclass
class PaymentResponse:
    """Response returned after a payment attempt.

    Attributes:
        success: Whether the payment was successful
        transaction_id: Unique transaction identifier
        message: Human-readable result message
        response_code: Machine-readable status code
    """
    success: bool
    transaction_id: str
    message: str
    response_code: ResponseCode

    @classmethod
    def approved(cls, transaction_id: str, amount: float) -> "PaymentResponse":
        """Create an approved payment response."""
        return cls(
            success=True,
            transaction_id=transaction_id,
            message=f"Payment of ${amount:.2f} approved",
            response_code=ResponseCode.APPROVED
        )

    @classmethod
    def declined(cls, transaction_id: str, reason: str = "Card declined by issuer") -> "PaymentResponse":
        """Create a declined payment response."""
        return cls(
            success=False,
            transaction_id=transaction_id,
            message=reason,
            response_code=ResponseCode.DECLINED
        )

    @classmethod
    def insufficient_funds(cls, transaction_id: str) -> "PaymentResponse":
        """Create an insufficient funds response."""
        return cls(
            success=False,
            transaction_id=transaction_id,
            message="Insufficient funds",
            response_code=ResponseCode.INSUFFICIENT_FUNDS
        )

    @classmethod
    def timeout(cls, transaction_id: str) -> "PaymentResponse":
        """Create a timeout response."""
        return cls(
            success=False,
            transaction_id=transaction_id,
            message="Network timeout - please try again",
            response_code=ResponseCode.TIMEOUT
        )
