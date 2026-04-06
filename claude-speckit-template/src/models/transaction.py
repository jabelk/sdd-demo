"""Transaction model for payment records."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from .response import ResponseCode


class TransactionStatus(Enum):
    """Transaction outcome status."""
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Transaction:
    """Represents a payment attempt and its outcome.

    Transactions are immutable after creation. They are stored in
    session memory only and not persisted to disk.

    Attributes:
        transaction_id: Unique identifier (UUID4 format with txn_ prefix)
        amount: Payment amount in USD
        masked_card: Last 4 digits of card (format: ****-****-****-NNNN)
        status: Transaction outcome (success/failed)
        failure_reason: Reason for failure (None if successful)
        response_code: Processor response code
        timestamp: When the transaction occurred
    """
    transaction_id: str
    amount: float
    masked_card: str
    status: TransactionStatus
    response_code: ResponseCode
    timestamp: datetime
    failure_reason: Optional[str] = None

    @classmethod
    def from_response(
        cls,
        response: "PaymentResponse",
        amount: float,
        masked_card: str
    ) -> "Transaction":
        """Create a Transaction from a PaymentResponse.

        Args:
            response: The payment processor response
            amount: The payment amount
            masked_card: The masked card number

        Returns:
            A new Transaction instance
        """
        from .response import PaymentResponse  # avoid circular import

        status = TransactionStatus.SUCCESS if response.success else TransactionStatus.FAILED
        failure_reason = None if response.success else response.message

        return cls(
            transaction_id=response.transaction_id,
            amount=amount,
            masked_card=masked_card,
            status=status,
            response_code=response.response_code,
            timestamp=datetime.now(),
            failure_reason=failure_reason
        )

    def is_successful(self) -> bool:
        """Check if the transaction was successful."""
        return self.status == TransactionStatus.SUCCESS
