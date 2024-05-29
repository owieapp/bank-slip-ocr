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

    def __init__(self):
        self.reference_number = ''
        self.transaction_date = ''
        self.from_user = ''
        self.to_user = ''
        self.to_account = ''
        self.amount = ''
        self.remarks = ''
