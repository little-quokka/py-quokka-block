from transaction import Transaction


class TransactionV1(Transaction):
    def __init__(self, id, amount, sender, recipient):
        self._id = id
        self._amount = amount
        self._sender = sender
        self._recipient = recipient

    @property
    def id(self):
        return self._id

    @property
    def amoun(self):
        return self._amount

    @property
    def sender(self):
        return self._sender

    @property
    def recipient(self):
        return self._recipient