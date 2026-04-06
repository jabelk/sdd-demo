"""Unit tests for the validator service."""

import pytest
from datetime import datetime


class TestLuhnValidation:
    """Tests for Luhn algorithm card number validation."""

    def test_valid_visa_card_passes_luhn(self, valid_card_number):
        """Valid Visa test card should pass Luhn check."""
        from src.services.validator import luhn_check
        assert luhn_check(valid_card_number) is True

    def test_invalid_card_fails_luhn(self, invalid_card_number):
        """Invalid card number should fail Luhn check."""
        from src.services.validator import luhn_check
        assert luhn_check(invalid_card_number) is False

    def test_valid_mastercard_passes_luhn(self):
        """Valid Mastercard test card should pass Luhn check."""
        from src.services.validator import luhn_check
        assert luhn_check("5500000000000004") is True

    def test_valid_amex_passes_luhn(self):
        """Valid Amex test card should pass Luhn check."""
        from src.services.validator import luhn_check
        assert luhn_check("340000000000009") is True

    def test_card_with_spaces_is_normalized(self):
        """Card numbers with spaces should be handled."""
        from src.services.validator import luhn_check
        assert luhn_check("4111 1111 1111 1111") is True

    def test_empty_card_number_fails(self):
        """Empty card number should fail."""
        from src.services.validator import luhn_check
        assert luhn_check("") is False

    def test_non_numeric_card_fails(self):
        """Card with non-numeric characters should fail."""
        from src.services.validator import luhn_check
        assert luhn_check("4111-1111-1111-1111") is False

    def test_card_too_short_fails(self):
        """Card number with fewer than 13 digits should fail."""
        from src.services.validator import luhn_check
        assert luhn_check("411111111111") is False  # 12 digits

    def test_card_too_long_fails(self):
        """Card number with more than 19 digits should fail."""
        from src.services.validator import luhn_check
        assert luhn_check("41111111111111111111") is False  # 20 digits


class TestExpiryValidation:
    """Tests for card expiry date validation."""

    def test_future_date_is_valid(self, valid_card_date):
        """Future expiry date should be valid."""
        from src.services.validator import validate_expiry
        month, year = valid_card_date
        assert validate_expiry(month, year) is True

    def test_past_date_is_invalid(self, expired_card_date):
        """Past expiry date should be invalid."""
        from src.services.validator import validate_expiry
        month, year = expired_card_date
        assert validate_expiry(month, year) is False

    def test_current_month_is_valid(self):
        """Current month should still be valid."""
        from src.services.validator import validate_expiry
        now = datetime.now()
        # Current month/year should be valid (card expires at end of month)
        year_2digit = now.year % 100
        assert validate_expiry(now.month, year_2digit) is True

    def test_invalid_month_zero(self):
        """Month 0 should be invalid."""
        from src.services.validator import validate_expiry
        assert validate_expiry(0, 30) is False

    def test_invalid_month_thirteen(self):
        """Month 13 should be invalid."""
        from src.services.validator import validate_expiry
        assert validate_expiry(13, 30) is False

    def test_negative_year_is_invalid(self):
        """Negative year should be invalid."""
        from src.services.validator import validate_expiry
        assert validate_expiry(12, -1) is False


class TestCVVValidation:
    """Tests for CVV validation."""

    def test_three_digit_cvv_is_valid(self, valid_cvv):
        """3-digit CVV should be valid."""
        from src.services.validator import validate_cvv
        assert validate_cvv(valid_cvv) is True

    def test_four_digit_cvv_is_valid(self, valid_cvv_amex):
        """4-digit CVV (Amex) should be valid."""
        from src.services.validator import validate_cvv
        assert validate_cvv(valid_cvv_amex) is True

    def test_two_digit_cvv_is_invalid(self, invalid_cvv):
        """2-digit CVV should be invalid."""
        from src.services.validator import validate_cvv
        assert validate_cvv(invalid_cvv) is False

    def test_five_digit_cvv_is_invalid(self):
        """5-digit CVV should be invalid."""
        from src.services.validator import validate_cvv
        assert validate_cvv("12345") is False

    def test_non_numeric_cvv_is_invalid(self):
        """Non-numeric CVV should be invalid."""
        from src.services.validator import validate_cvv
        assert validate_cvv("12a") is False

    def test_empty_cvv_is_invalid(self):
        """Empty CVV should be invalid."""
        from src.services.validator import validate_cvv
        assert validate_cvv("") is False


class TestAmountValidation:
    """Tests for payment amount validation."""

    def test_valid_amount(self, valid_amount):
        """Valid amount should pass."""
        from src.services.validator import validate_amount
        assert validate_amount(valid_amount) is True

    def test_minimum_amount(self):
        """Minimum amount ($0.01) should be valid."""
        from src.services.validator import validate_amount
        assert validate_amount(0.01) is True

    def test_maximum_amount(self):
        """Maximum amount ($10,000) should be valid."""
        from src.services.validator import validate_amount
        assert validate_amount(10000.00) is True

    def test_zero_amount_is_invalid(self, invalid_amount_zero):
        """Zero amount should be invalid."""
        from src.services.validator import validate_amount
        assert validate_amount(invalid_amount_zero) is False

    def test_negative_amount_is_invalid(self, invalid_amount_negative):
        """Negative amount should be invalid."""
        from src.services.validator import validate_amount
        assert validate_amount(invalid_amount_negative) is False

    def test_amount_over_maximum_is_invalid(self, invalid_amount_too_large):
        """Amount over $10,000 should be invalid."""
        from src.services.validator import validate_amount
        assert validate_amount(invalid_amount_too_large) is False

    def test_amount_just_under_minimum_is_invalid(self):
        """Amount just under minimum should be invalid."""
        from src.services.validator import validate_amount
        assert validate_amount(0.009) is False

    def test_amount_just_over_maximum_is_invalid(self):
        """Amount just over maximum should be invalid."""
        from src.services.validator import validate_amount
        assert validate_amount(10000.01) is False
