from dataclasses import dataclass


@dataclass
class ReceiptModel:
    reference_number: str
    transaction_date: str
    from_user: str
    to_user: str
    to_account: str
    amount: str
    remarks: str
