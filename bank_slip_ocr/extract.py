import cv2
import numpy as np
import pytesseract
import xmltodict

from .banks.bml import process as bml_process


def preprocess_image(img):
    # Convert to grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dilation
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)

    # Noise reduction
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Save the processed image
    cv2.imwrite('datasets/preprocessed.jpg', img)

    return img


def extract_bank_slip_data(img) -> dict:
    stringdata = pytesseract.image_to_string(img, lang='eng')
    df = pytesseract.image_to_data(img, output_type='data.frame', lang='eng', config='--oem 3 --psm 6')

    if ('Bank of Maldives' in stringdata):
        return bml_process(df)

    return 'Unable to identify bank!'


if __name__ == "__main__":
    with open("datasets/bank_slip_3.jpg", "rb") as f:
        file_bytes = np.frombuffer(f.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        preprocessed_img = preprocess_image(image)

        data = extract_bank_slip_data(image)
        # print(data.to_string())
