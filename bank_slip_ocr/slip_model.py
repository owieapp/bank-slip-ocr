from dataclasses import dataclass


@dataclass
class SlipModel:
    reference_number: str
    transaction_date: str
    from_user: str
    to_user: str
    to_account: str
    amount: str
    remarks: str
