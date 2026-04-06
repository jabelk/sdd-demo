"""Integration tests for end-to-end payment flows."""

import pytest
from unittest.mock import patch


class TestPaymentFlow:
    """Integration tests for the complete payment flow."""

    def test_valid_payment_full_flow(self, valid_card_number, valid_amount):
        """Test complete payment flow with valid inputs."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.models.response import ResponseCode
        from src.cli.display import mask_card_number

        # Create card
        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        # Process payment
        with patch("src.services.processor.time.sleep"):
            response = process_payment(card, valid_amount)

        # Verify response
        assert response.success is True
        assert response.response_code == ResponseCode.APPROVED
        assert response.transaction_id.startswith("txn_")

        # Verify card masking
        masked = mask_card_number(valid_card_number)
        assert "****-****-****-1111" == masked
        assert valid_card_number not in masked

    def test_payment_flow_with_all_validation(self):
        """Test that validation is performed before processing."""
        from src.services.validator import luhn_check, validate_expiry, validate_cvv, validate_amount

        # Valid inputs
        card_number = "4111111111111111"
        expiry_month, expiry_year = 12, 30
        cvv = "123"
        amount = 50.00

        # All validations should pass
        assert luhn_check(card_number) is True
        assert validate_expiry(expiry_month, expiry_year) is True
        assert validate_cvv(cvv) is True
        assert validate_amount(amount) is True

    def test_payment_with_invalid_card_rejected_before_processing(self, invalid_card_number):
        """Invalid card should be rejected during validation, not processing."""
        from src.services.validator import luhn_check

        # Luhn check should catch invalid card
        assert luhn_check(invalid_card_number) is False

    def test_payment_with_expired_card_rejected(self, expired_card_date):
        """Expired card should be rejected during validation."""
        from src.services.validator import validate_expiry

        month, year = expired_card_date
        assert validate_expiry(month, year) is False

    def test_card_number_never_appears_in_full(self, valid_card_number, valid_amount):
        """Card number should never appear in full in any output."""
        from src.services.processor import process_payment
        from src.models.card import Card
        from src.cli.display import mask_card_number

        card = Card(
            number=valid_card_number,
            expiry_month=12,
            expiry_year=30,
            cvv="123"
        )

        with patch("src.services.processor.time.sleep"):
            response = process_payment(card, valid_amount)

        # Check response doesn't contain full card number
        assert valid_card_number not in response.message
        assert valid_card_number not in response.transaction_id

        # Masked version should not equal original
        masked = mask_card_number(valid_card_number)
        assert masked != valid_card_number
        assert valid_card_number not in masked
