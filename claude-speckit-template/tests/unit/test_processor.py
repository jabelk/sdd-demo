"""Unit tests for the payment processor service."""

import pytest
import re
from unittest.mock import patch


class TestPaymentProcessor:
    """Tests for the payment processor service."""

    def test_successful_payment_returns_approved_response(self, valid_card_number, valid_amount):
        """Valid payment details should result in approved response."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.models.response import ResponseCode

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):  # Skip delay in tests
            response = process_payment(card, valid_amount)

        assert response.success is True
        assert response.response_code == ResponseCode.APPROVED
        assert "approved" in response.message.lower()

    def test_transaction_id_has_uuid_format(self, valid_card_number, valid_amount):
        """Transaction ID should follow UUID format with txn_ prefix."""
        from src.services.processor import process_payment
        from src.models.card import Card

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):
            response = process_payment(card, valid_amount)

        # Transaction ID should start with txn_ prefix
        assert response.transaction_id.startswith("txn_")

        # Extract UUID part and validate format
        uuid_part = response.transaction_id[4:]  # Remove "txn_" prefix
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        assert re.match(uuid_pattern, uuid_part, re.IGNORECASE)

    def test_each_payment_gets_unique_transaction_id(self, valid_card_number, valid_amount):
        """Each payment should receive a unique transaction ID."""
        from src.services.processor import process_payment
        from src.models.card import Card

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):
            response1 = process_payment(card, valid_amount)
            response2 = process_payment(card, valid_amount)

        assert response1.transaction_id != response2.transaction_id

    def test_payment_includes_processing_delay(self, valid_card_number, valid_amount):
        """Payment processing should include a delay."""
        from src.services.processor import process_payment
        from src.models.card import Card

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep") as mock_sleep:
            process_payment(card, valid_amount)

        # Verify sleep was called with a value between 1-2 seconds
        mock_sleep.assert_called()
        delay = mock_sleep.call_args[0][0]
        assert 1.0 <= delay <= 2.0


class TestFailureTriggers:
    """Tests for payment failure trigger scenarios (amount-based)."""

    def test_declined_trigger_amount_001(self, valid_card_number):
        """Amount of $0.01 should trigger declined response."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.models.response import ResponseCode

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):
            response = process_payment(card, 0.01)

        assert response.success is False
        assert response.response_code == ResponseCode.DECLINED
        assert "declined" in response.message.lower()

    def test_insufficient_funds_trigger(self, valid_card_number, insufficient_funds_amount):
        """Amount of 999.99 should trigger insufficient funds response."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.models.response import ResponseCode

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):
            response = process_payment(card, insufficient_funds_amount)

        assert response.success is False
        assert response.response_code == ResponseCode.INSUFFICIENT_FUNDS
        assert "insufficient" in response.message.lower()

    def test_timeout_trigger_amount_77777(self, valid_card_number):
        """Amount of $777.77 should trigger timeout with extended delay."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.models.response import ResponseCode

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep") as mock_sleep:
            response = process_payment(card, 777.77)

        assert response.success is False
        assert response.response_code == ResponseCode.TIMEOUT
        assert "timeout" in response.message.lower()

        # Timeout should have a 5-second delay
        mock_sleep.assert_called()
        delay = mock_sleep.call_args[0][0]
        assert delay == 5.0
