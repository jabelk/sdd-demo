"""Unit tests for the transaction history service."""

import pytest
from datetime import datetime

from src.services.history import TransactionHistory
from src.models.transaction import Transaction, TransactionStatus
from src.models.response import ResponseCode


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing."""
    return Transaction(
        transaction_id="txn_test-1234",
        amount=50.00,
        masked_card="****-****-****-1111",
        status=TransactionStatus.SUCCESS,
        response_code=ResponseCode.APPROVED,
        timestamp=datetime.now(),
        failure_reason=None
    )


@pytest.fixture
def failed_transaction():
    """Create a failed transaction for testing."""
    return Transaction(
        transaction_id="txn_test-5678",
        amount=999.99,
        masked_card="****-****-****-2222",
        status=TransactionStatus.FAILED,
        response_code=ResponseCode.INSUFFICIENT_FUNDS,
        timestamp=datetime.now(),
        failure_reason="Insufficient funds"
    )


class TestTransactionHistory:
    """Tests for the TransactionHistory class."""

    def test_new_history_is_empty(self):
        """New history should have no transactions."""
        history = TransactionHistory()
        assert history.count() == 0
        assert history.list() == []

    def test_add_transaction(self, sample_transaction):
        """Should be able to add a transaction."""
        history = TransactionHistory()
        history.add(sample_transaction)

        assert history.count() == 1
        assert sample_transaction in history.list()

    def test_add_multiple_transactions(self, sample_transaction, failed_transaction):
        """Should be able to add multiple transactions."""
        history = TransactionHistory()
        history.add(sample_transaction)
        history.add(failed_transaction)

        assert history.count() == 2

    def test_list_returns_newest_first(self, sample_transaction, failed_transaction):
        """List should return transactions in reverse chronological order."""
        history = TransactionHistory()
        history.add(sample_transaction)  # Added first
        history.add(failed_transaction)  # Added second

        transactions = history.list()

        # Most recent (failed_transaction) should be first
        assert transactions[0] == failed_transaction
        assert transactions[1] == sample_transaction

    def test_clear_removes_all_transactions(self, sample_transaction, failed_transaction):
        """Clear should remove all transactions."""
        history = TransactionHistory()
        history.add(sample_transaction)
        history.add(failed_transaction)

        history.clear()

        assert history.count() == 0
        assert history.list() == []

    def test_count_returns_correct_number(self, sample_transaction):
        """Count should return the correct number of transactions."""
        history = TransactionHistory()

        assert history.count() == 0

        history.add(sample_transaction)
        assert history.count() == 1

        history.add(sample_transaction)
        assert history.count() == 2

        history.add(sample_transaction)
        assert history.count() == 3
