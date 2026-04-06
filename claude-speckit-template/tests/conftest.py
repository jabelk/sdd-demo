"""Shared test fixtures for the payment CLI simulator."""

import pytest
from datetime import datetime


@pytest.fixture
def valid_card_number():
    """A valid card number that passes Luhn check (Visa test number)."""
    return "4111111111111111"


@pytest.fixture
def invalid_card_number():
    """An invalid card number that fails Luhn check."""
    return "1234567890123456"


@pytest.fixture
def expired_card_date():
    """An expired card date."""
    return (1, 20)  # January 2020


@pytest.fixture
def valid_card_date():
    """A valid future card date."""
    return (12, 30)  # December 2030


@pytest.fixture
def valid_cvv():
    """A valid 3-digit CVV."""
    return "123"


@pytest.fixture
def valid_cvv_amex():
    """A valid 4-digit CVV (Amex style)."""
    return "1234"


@pytest.fixture
def invalid_cvv():
    """An invalid CVV (too short)."""
    return "12"


@pytest.fixture
def valid_amount():
    """A valid payment amount."""
    return 50.00


@pytest.fixture
def invalid_amount_negative():
    """An invalid negative amount."""
    return -10.00


@pytest.fixture
def invalid_amount_zero():
    """An invalid zero amount."""
    return 0.00


@pytest.fixture
def invalid_amount_too_large():
    """An amount exceeding the maximum limit."""
    return 15000.00


@pytest.fixture
def declined_card_number():
    """Card number that triggers declined response (ends in 0001)."""
    return "4111111111110001"


@pytest.fixture
def timeout_card_number():
    """Card number that triggers timeout response (ends in 0002)."""
    return "4111111111110002"


@pytest.fixture
def insufficient_funds_amount():
    """Amount that triggers insufficient funds response."""
    return 999.99
