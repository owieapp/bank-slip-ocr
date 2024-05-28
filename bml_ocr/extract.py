import easyocr
import Levenshtein
from PIL import Image
from io import BytesIO


def is_white(pixel):
    for color in pixel:
        if color < 250:
            return False

    return True


def find_y_positions_of_gray_lines(byte_data, start_y=0):
    """
    Find the y axis values for gray lines in the image

    Args:
        byte_data (bytes): Image byte data
    """
    image = Image.open(BytesIO(byte_data))
    line_positions = []

    for y in range(start_y, image.height):
        x_pos = 134
        pixel = image.getpixel((x_pos, y))

        if not is_white(pixel):
            flag = True

            for x in range(x_pos, x_pos + 50):
                pixel = image.getpixel((x, y))
                if is_white(pixel):
                    flag = False
                    break

            if flag:
                line_positions.append(y)
                y += 10

    return line_positions


def find_closest_match(data, word):
    texts = [entry[1] for entry in data]
    distances = [Levenshtein.distance(text, word) for text in texts]
    min_distance = min(distances)
    closest_match_index = distances.index(min_distance)
    return data[closest_match_index]


def extract_receipt_data(byte_data):
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(byte_data)
    closest_match = find_closest_match(result, 'Message')

    line_positions = find_y_positions_of_gray_lines(byte_data, closest_match[0][0][1])
    print(line_positions)
    # keys = ['Reference', 'Transaction date', 'From', 'To', 'Amount', 'Remarks']


if __name__ == '__main__':
    with open('datasets/receipt_3.jpg', 'rb') as f:
        extract_receipt_data(f.read())
