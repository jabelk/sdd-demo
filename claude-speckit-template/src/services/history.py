"""Transaction history service for session-based storage."""

from src.models.transaction import Transaction


class TransactionHistory:
    """In-memory storage for transaction history.

    Transactions are stored for the duration of the session only
    and are not persisted to disk.
    """

    def __init__(self) -> None:
        """Initialize an empty transaction history."""
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        """Add a transaction to the history.

        Args:
            transaction: The transaction to add
        """
        self._transactions.append(transaction)

    def list(self) -> list[Transaction]:
        """Get all transactions, newest first.

        Returns:
            List of transactions in reverse chronological order
        """
        return list(reversed(self._transactions))

    def count(self) -> int:
        """Get the number of transactions.

        Returns:
            The total number of transactions
        """
        return len(self._transactions)

    def clear(self) -> None:
        """Clear all transactions from history."""
        self._transactions.clear()
