import pandas as pd

from bank_slip_ocr.slip_model import SlipModel


def process(df: pd.DataFrame):
    print('Processing Bank of Maldives data...')
    text_col = pd.DataFrame(df.loc[:, 'text'])

    slip = SlipModel(
        reference_number=None,
        transaction_date=None,
        from_user=None,
        to_user=None,
        to_account=None,
        amount=None,
        remarks=None
    )

    for i, j in text_col.iterrows():
        print(j['text'])
