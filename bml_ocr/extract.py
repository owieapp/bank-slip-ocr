import random
from typing import Callable

import easyocr
import Levenshtein
from PIL import Image
from io import BytesIO

from bml_ocr.receipt_model import ReceiptModel


def is_white(pixel):
    for color in pixel:
        if color < 250:
            return False

    return True


def is_black(pixel):
    for color in pixel:
        if color > 35:
            return False

    return True


def is_black_or_white(image: Image) -> bool:
    """
    Returns true if white
    Args:
        image: image

    Returns: if white

    """
    width, height = image.size

    white = 0
    black = 0

    for x in range(500):
        # Generate random coordinates
        x_cor = random.randint(0, width - 1)
        y_cor = random.randint(0, height - 1)
        pixel = image.getpixel((x_cor, y_cor))

        if is_white(pixel):
            white += 1
        elif is_black(pixel):
            black += 1

    return white > black


def find_y_values_of_gray_lines(color_detector: Callable, byte_data, start_y=0, ):
    """
    Find the y axis values for gray lines in the image

    Args:
        color_detector: the function that can detect lines
        byte_data (bytes): Image byte data
        start_y (int): Starting y axis value when iterating pixels
    """
    image = Image.open(BytesIO(byte_data))
    y_values = []  # List of y axis values for gray lines

    y = start_y
    while y < image.height:
        x_pos = 134
        pixel = image.getpixel((x_pos, y))

        if not color_detector(pixel):
            flag = True

            for x in range(x_pos, x_pos + 50):
                pixel = image.getpixel((x, y))
                if color_detector(pixel):
                    flag = False
                    break

            if flag:
                y_values.append(y)
                y += 10
            else:
                y += 1
        else:
            y += 1

    return y_values


def find_closest_match(data, word):
    texts = [entry[1] for entry in data]
    distances = [Levenshtein.distance(text, word) for text in texts]
    min_distance = min(distances)
    closest_match_index = distances.index(min_distance)
    return data[closest_match_index]


def find_values_between(start_y, end_y, data):
    values = []
    for entry in data:
        if start_y < entry[0][0][1] < end_y:
            values.append(entry[1])

    return values


def extract_receipt_data(byte_data):
    """Extracts text from receipt data and returns a dictionary

    Args:
        byte_data (bytes): Image byte data

    Returns:
        ReceiptModel: Extracted receipt data
    """
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(byte_data)
    closest_match = find_closest_match(result, 'Message')

    image = Image.open(BytesIO(byte_data))
    bg_is_white = is_black_or_white(image)
    if bg_is_white:
        detector = is_white
    else:
        detector = is_black

    lines_y_values = find_y_values_of_gray_lines(detector, byte_data, closest_match[0][0][1])

    keys = [
        ('Reference', 0, 1),
        ('Transaction date', 1, 2),
        ('From', 2, 3),
        ('To', 3, 4),
        ('Amount', 4, 5),
        ('Remarks', 5, 6)
    ]

    receipt = ReceiptModel()
    for key in keys:
        text = key[0]
        start_y = lines_y_values[key[1]]
        end_y = lines_y_values[key[2]]

        closest_match = find_closest_match(result, text)
        section_values = find_values_between(start_y, end_y, result)
        # Remove key from section values
        if len(section_values) > 0:
            index = section_values.index(closest_match[1])
            section_values.pop(index)

        if text == 'Reference':
            receipt.reference_number = section_values[0]
        elif text == 'Transaction date':
            receipt.transaction_date = section_values[0]
        elif text == 'From':
            receipt.from_user = section_values[0]
        elif text == 'To':
            receipt.to_user = section_values[0]
            receipt.to_account = section_values[1]
        elif text == 'Amount':
            receipt.amount = section_values[0]
        elif text == 'Remarks':
            if len(section_values) > 0:
                combined_text = ' '.join(section_values)
                receipt.remarks = combined_text

    return receipt


if __name__ == '__main__':
    import os
    files = os.listdir('data')

    with open("data/18b.jpg", 'rb') as f:
        receipt: ReceiptModel = extract_receipt_data(f.read())

    # success = 0
    # failed = 0
    # for file in files:
    #     _path = f"data/{file}"
    #
    #     with open(_path, 'rb') as f:
    #         try:
    #             receipt: ReceiptModel = extract_receipt_data(f.read())
    #             success += 1
    #             print(f"Succeeded {receipt} {_path}")
    #         except Exception as e:
    #             failed += 1
    #             print(f"Failed {e} {_path}")
    #
    # print(f"Success: {success}")
    # print(f"Failed: {failed}")
