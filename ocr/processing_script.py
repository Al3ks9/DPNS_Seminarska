import Levenshtein
import pandas as pd
import cv2
import numpy as np

source_folder = './images/'
df = pd.read_csv('new__out.csv', encoding_errors='ignore', na_values=None, keep_default_na=False)
id_df = df.groupby('id')


def levenshtein_accuracy(ocr_text, actual_text):
    distance = Levenshtein.distance(ocr_text.lower(), actual_text.lower())
    max_length = max(len(actual_text), len(ocr_text))
    accuracy = (max_length - distance) / max_length
    return accuracy


def preprocess_image(image_id):
    path = source_folder + image_id + '.jpg'
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(thresh, kernel, iterations=1)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
    return eroded_image


def process_true_text(image_id):
    filtered_rows = id_df.get_group(image_id)
    text = list(filtered_rows['text'])
    text.sort()
    spaced_list = [line.split(' ') for line in text]
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def process_tesseract_text(string):
    if string == '':
        return ''
    text_list = string.split('\n')
    text_list.sort()
    spaced_list = [line.split(' ') for line in text_list if line != '']
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def process_easyocr_text(results):
    res = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
    text_list = res['text'].values.tolist()
    text_list.sort()
    spaced_list = [line.split(' ') for line in text_list if line != '']
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def compare_accuracy(image_id, original_output, processed_output):
    true_text = process_true_text(image_id)
    original_acc = levenshtein_accuracy(original_output, true_text)
    processed_acc = levenshtein_accuracy(processed_output, true_text)
    if original_acc > processed_acc:
        return 1, original_acc
    else:
        return 0, processed_acc
