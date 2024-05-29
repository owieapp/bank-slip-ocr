# BML OCR

A package to extract details from BML transfer receipts.

## How it works

The `extract_receipt_data` function is where OCR and data extraction takes place. This function returns a [ReceiptModel](https://github.com/owieapp/bml_ocr/blob/main/bml_ocr/receipt_model.py).

### 1. Text recognition using EasyOCR

- The `readtext` method will take in Image data as bytes and returns the result set containing a list of tuples. Eg.

```python
(
    # Border positions of the text boxes
    [
      [47, 689],
      [184, 689],
      [184, 731],
      [47, 731]
    ],
    # Text recognized
    'Message',
    # Confidence level
    0.9999883302470524
)
```

### 2. Finding the 'Messages' keyword from the OCR results

- In order to find this, I calculate the Lavenshtein distance from the result set from Step 1 for the 'Messages' keyword to get the most probable result.
- This result is used to find the y axis value of the text border used in Step 3

### 3. Detecting all the gray lines

- This is the separater between text sections.
- Finding these involves looping through the pixels in the y axis and checking whether the background is white or not.
- The loop will start from the y value from Step 2 which helps in retieving the gray line above 'Reference' section.
- If the background is not white then we check horizontally if its constant. Those that are constant is returned as gray lines.

### 4. Extracting relevant data for sections.

- Now that we have the gray line positions and the results from OCR, we use this to categorize the data into its respective sections based on the gray line above and below the section.
- The categorized data is then mapped to a `ReceiptModel` as follows:

```python
ReceiptModel(
    reference_number='BLAZ876699558640',
    transaction_date='25/05/2024 15.20',
    from_user='NAFFAH ARASHEED',
    to_user='Haisham',
    to_account='7730000203614',
    amount='MVR 1.00',
    remarks='Lorem ipsum dolor sit amet amegakure hokage shinobi'
)
```

# Credits

- @nishaalnaseer: For his original implementation of finding gray lines [BML-OCR](https://github.com/nishaalnaseer/BML-OCR)
