"""Payment processor service for simulating payment processing."""

import time
import uuid
import random
from typing import Optional, Tuple

from src.models.card import Card
from src.models.response import PaymentResponse, ResponseCode


def generate_transaction_id() -> str:
    """Generate a unique transaction ID.

    Returns:
        A unique transaction ID in format: txn_<uuid4>
    """
    return f"txn_{uuid.uuid4()}"


def check_failure_triggers(card: Card, amount: float) -> Tuple[bool, Optional[str]]:
    """Check if the payment should trigger a specific failure scenario.

    Args:
        card: The card being used for payment
        amount: The payment amount

    Returns:
        Tuple of (should_fail, failure_type) where failure_type is one of:
        - "declined" for amount 0.01
        - "insufficient_funds" for amount 999.99
        - "timeout" for amount 777.77
        - None if no trigger matched
    """
    # Trigger by specific amounts (easier to test)
    if amount == 0.01:
        return (True, "declined")

    if amount == 999.99:
        return (True, "insufficient_funds")

    if amount == 777.77:
        return (True, "timeout")

    return (False, None)


def process_payment(card: Card, amount: float) -> PaymentResponse:
    """Process a payment simulation.

    This simulates payment processing with realistic delays and
    supports trigger values for testing failure scenarios.

    Args:
        card: The card to charge
        amount: The amount to charge

    Returns:
        PaymentResponse with the result of the payment attempt
    """
    transaction_id = generate_transaction_id()

    # Check for failure triggers
    should_fail, failure_type = check_failure_triggers(card, amount)

    if should_fail:
        if failure_type == "declined":
            # Normal processing delay for declined cards
            time.sleep(random.uniform(1.0, 2.0))
            return PaymentResponse.declined(transaction_id)

        elif failure_type == "insufficient_funds":
            # Normal processing delay
            time.sleep(random.uniform(1.0, 2.0))
            return PaymentResponse.insufficient_funds(transaction_id)

        elif failure_type == "timeout":
            # Extended delay for timeout simulation
            time.sleep(5.0)
            return PaymentResponse.timeout(transaction_id)

    # Normal successful payment with 1-2 second delay
    time.sleep(random.uniform(1.0, 2.0))
    return PaymentResponse.approved(transaction_id, amount)
